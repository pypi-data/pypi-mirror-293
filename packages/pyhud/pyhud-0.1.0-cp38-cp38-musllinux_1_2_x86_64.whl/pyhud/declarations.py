import ast
from typing import List, Optional, Union
from uuid import UUID

from .schemas.events import CodeBlockType, FunctionDeclaration


class Declaration:
    __match_args__ = (
        "function_id",
        "name",
        "path",
        "start_line",
        "end_line",
        "is_async",
        "source_code_hash",
        "code_block_type",
    )

    def __init__(
        self,
        function_id: UUID,
        name: str,
        path: str,
        start_line: int,
        end_line: Optional[int],
        is_async: bool,
        source_code_hash: str,
        code_block_type: CodeBlockType,
    ):
        self.function_id = function_id
        self.name = name
        self.path = path
        self.start_line = start_line
        self.end_line = end_line
        self.is_async = is_async
        self.source_code_hash = source_code_hash
        self.code_block_type = code_block_type

    @classmethod
    def from_function_node(
        cls,
        function_id: UUID,
        node: Union[ast.FunctionDef, ast.AsyncFunctionDef],
        source_code_hash: str,
        path: str,
        is_async: bool,
    ) -> "Declaration":
        return cls(
            function_id,
            node.name,
            path,
            node.lineno,
            getattr(node, "end_lineno", None),
            is_async,
            source_code_hash,
            CodeBlockType.FUNCTION,
        )

    @classmethod
    def from_class_node(
        cls,
        class_id: UUID,
        node: ast.ClassDef,
        source_code_hash: str,
        path: str,
    ) -> "Declaration":
        return cls(
            class_id,
            node.name,
            path,
            node.lineno,
            getattr(node, "end_lineno", None),
            False,
            source_code_hash,
            CodeBlockType.CLASS,
        )

    def for_request(self) -> "FunctionDeclaration":
        return FunctionDeclaration(
            self.path,
            str(self.function_id),
            self.is_async,
            self.name,
            self.source_code_hash,
            self.start_line,
            self.end_line,
            self.code_block_type,
        )


class DeclarationsAggregator:
    def __init__(self) -> None:
        self.declarations = []  # type: List[Declaration]

    def add_declaration(self, declaration: Declaration) -> None:
        self.declarations.append(declaration)

    def get_declarations(self) -> List[FunctionDeclaration]:
        return [declaration.for_request() for declaration in self.declarations]

    def clear(self) -> None:
        self.declarations = []
