import ast
import os
import sys
from hashlib import sha1
from importlib.abc import Loader, PathEntryFinder
from importlib.machinery import FileFinder, ModuleSpec, SourceFileLoader
from random import randint
from types import CodeType
from typing import Any, List, Mapping, Optional, Tuple, Type, Union, cast
from uuid import uuid4

from ._internal import worker_queue
from .config import config
from .declarations import Declaration
from .exception_handler import install_exception_handler
from .logging import internal_logger
from .run_mode import should_run_hud

paths_to_wrap = [
    os.getcwd(),
]  # type: List[str]


file_path = getattr(sys.modules["__main__"], "__file__", None)
if file_path:
    paths_to_wrap.append(os.path.dirname(os.path.abspath(file_path)))


class ASTTransformer(ast.NodeTransformer):
    def __init__(self, path: str, lines: List[bytes]) -> None:
        self.path = path
        self.lines = lines
        self.compiler_flags = 0

    def get_function_source_code_hash(self, node: Union[ast.stmt, ast.expr]) -> str:
        if (sys.version_info.major, sys.version_info.minor) < (3, 8):
            return sha1(ast.dump(node).encode()).hexdigest()
        else:
            start_line = node.lineno - 1
            end_line = cast(int, node.end_lineno) - 1
            source_code = b"\n".join(self.lines[start_line : end_line + 1])
            return sha1(source_code).hexdigest()

    def visit_FunctionDef(self, node: ast.FunctionDef) -> ast.FunctionDef:
        source_code_hash = self.get_function_source_code_hash(node)
        node.args = self.visit(node.args)
        function_id = uuid4()
        stmts = ast.parse(
            'with HudContextManager("{}"):\n    pass'.format(function_id)
        ).body  # type: List[ast.stmt]
        with_stmt = cast(ast.With, stmts[-1])
        with_stmt.body = [self.visit(stmt) for stmt in node.body]
        node.body = [*stmts]
        node.decorator_list = [
            self.visit(decorator) for decorator in node.decorator_list
        ]
        worker_queue.append(
            Declaration.from_function_node(
                function_id, node, source_code_hash, self.path, is_async=False
            )
        )
        return node

    def visit_AsyncFunctionDef(
        self, node: ast.AsyncFunctionDef
    ) -> ast.AsyncFunctionDef:
        source_code_hash = self.get_function_source_code_hash(node)
        node.args = self.visit(node.args)
        function_id = uuid4()
        with_stmt = cast(
            ast.With,
            ast.parse(
                'with HudContextManager("{}"):\n    pass'.format(function_id)
            ).body[0],
        )  # type: ast.With
        with_stmt.body = [self.visit(stmt) for stmt in node.body]
        node.body = [with_stmt]
        node.decorator_list = [
            self.visit(decorator) for decorator in node.decorator_list
        ]
        worker_queue.append(
            Declaration.from_function_node(
                function_id, node, source_code_hash, self.path, is_async=True
            )
        )
        return node

    def visit_Lambda(self, node: ast.Lambda) -> ast.Lambda:
        node.args = self.visit(node.args)
        node.body = self.visit(node.body)
        return node

    def visit_ClassDef(self, node: ast.ClassDef) -> Any:
        source_code_hash = self.get_function_source_code_hash(node)
        class_id = uuid4()
        worker_queue.append(
            Declaration.from_class_node(class_id, node, source_code_hash, self.path)
        )
        return self.generic_visit(node)

    def visit_ImportFrom(self, node: ast.ImportFrom) -> Any:
        # When passing an AST to the `compile` function, the `__future__` imports are not parsed
        # and the compiler flags are not set. This is a workaround to set the compiler flags,
        # and removing the invalid imports.
        if node.module == "__future__":
            import __future__

            for name in node.names:
                feature = getattr(__future__, name.name)
                self.compiler_flags |= feature.compiler_flag
            return None
        return self.generic_visit(node)


def should_wrap_file(path: str) -> bool:
    return path in paths_to_wrap


def should_wrap_module(fullname: str) -> bool:
    if fullname in config.modules_to_trace:
        return True
    for module in config.modules_to_trace:
        if fullname.startswith("{}.".format(module)):
            return True
    return False


class MyFileFinder(FileFinder):
    def __repr__(self) -> str:
        return "MyFileFinder('{}')".format(self.path)

    def __init__(
        self,
        path: str,
        *loader_details: Tuple[Type[Loader], List[str]],
        override: bool = False
    ) -> None:
        if not should_wrap_file(os.path.abspath(path)) and not override:
            raise ImportError("Not wrapping path: {}".format(path))
        super().__init__(path, *loader_details)

    def find_spec(self, fullname: str, *args: Any) -> Optional[ModuleSpec]:
        spec = super().find_spec(fullname, *args)
        if spec is not None and spec.submodule_search_locations is not None:
            paths_to_wrap.extend(spec.submodule_search_locations)
        return spec


class ModuleFinder(MyFileFinder):
    def __init__(self, path: str, original_finder: PathEntryFinder) -> None:
        self.path = path
        self.original_finder = original_finder
        super().__init__(path, (MySourceLoader, [".py"]), override=True)

    def __repr__(self) -> str:
        return "ModuleFinder('{}', original_finder={})".format(
            self.path, self.original_finder
        )

    def find_spec(self, fullname: str, *args: Any) -> Optional[ModuleSpec]:
        spec = None
        if should_wrap_module(fullname):
            spec = super().find_spec(fullname, *args)
        if spec is not None:
            if spec.origin is not None and spec.origin not in paths_to_wrap:
                paths_to_wrap.append(os.path.dirname(spec.origin))
            return spec
        if self.original_finder is not None:
            return self.original_finder.find_spec(fullname, *args)


class MySourceLoader(SourceFileLoader):
    def path_stats(self, path: str) -> Mapping[str, Any]:
        stats = super().path_stats(path)
        stats["mtime"] -= randint(  # type: ignore
            1, 500
        )  # This manipulation allows bytecode caching to work for the edited module, without conflicting with the original module
        return stats

    def get_data(self, path: str) -> bytes:
        if path.endswith(".pyc"):
            raise OSError("No .pyc files allowed")
        return super().get_data(path)

    def source_to_code(  # type: ignore[override]
        self, data: bytes, path: str, *, _optimize: int = -1
    ) -> CodeType:
        try:
            internal_logger.debug("Monitoring file: {}".format(path))
            tree = cast(
                ast.Module,
                compile(
                    data,
                    path,
                    "exec",
                    flags=ast.PyCF_ONLY_AST,
                    dont_inherit=True,
                    optimize=_optimize,
                ),
            )  # type: ast.Module
            transformer = ASTTransformer(path, data.splitlines())
            tree = transformer.visit(tree)
            tree.body = [
                *ast.parse("from pyhud.native import HudContextManager\n").body,
                *tree.body,
            ]
            return cast(
                CodeType,
                compile(
                    tree,
                    path,
                    "exec",
                    flags=transformer.compiler_flags,
                    dont_inherit=True,
                    optimize=_optimize,
                ),
            )
        except Exception as e:
            internal_logger.error(
                "Error while transforming AST on file: {}, error: {}".format(path, e)
            )
            return super().source_to_code(data, path)


def module_hook(path: str) -> ModuleFinder:
    original_finder = None
    for hook in sys.path_hooks:
        if hook is not module_hook:
            try:
                original_finder = hook(path)
            except ImportError:
                continue
            return ModuleFinder(
                path, original_finder=cast(PathEntryFinder, original_finder)
            )

    raise ImportError("No module finder found for path: {}".format(path))


hook_set = False


def set_hook() -> None:
    global hook_set
    if hook_set:
        return
    if should_run_hud():
        hook_set = True

        if not config.disable_exception_handler:
            install_exception_handler()

        for path in paths_to_wrap:
            if path in sys.path_importer_cache:
                del sys.path_importer_cache[path]
        for path in sys.path:
            if path in sys.path_importer_cache:
                del sys.path_importer_cache[path]
        sys.path_hooks.insert(0, MyFileFinder.path_hook((MySourceLoader, [".py"])))
        sys.path_hooks.insert(0, module_hook)
