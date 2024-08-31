import ast
from typing import Any, Generator, Tuple


class PydanticFieldChecker(ast.NodeVisitor):
    def __init__(self, tree: ast.AST) -> None:
        self.tree = tree
        self.issues = []

    def run(self) -> Generator[Tuple[int, int, str, type], None, None]:
        self.visit(self.tree)
        yield from self.issues

    def visit_AnnAssign(self, node: ast.AnnAssign) -> Any:
        self.check_field(node)
        self.generic_visit(node)

    # .AnnAssign(target=Name(id='name', ctx=Store(), lineno=5, col_offset=4, end_lineno=5, end_col_offset=8),
    # annotation=Name(id='str', ctx=Load(), lineno=5, col_offset=10, end_lineno=5, end_col_offset=13),
    # value=Call(func=Name(id='Field', ctx=Load(), lineno=5, col_offset=16, end_lineno=5, end_col_offset=21),
    # args=[],
    # keywords=[], lineno=5, col_offset=16, end_lineno=5, end_col_offset=23),
    # simple=1, lineno=5, col_offset=4, end_lineno=5, end_col_offset=23)

    def check_field(self, node: ast.AnnAssign) -> None:
        if (
            isinstance(node.value, ast.Call)
            and isinstance(node.value.func, ast.Name)
            and node.value.func.id == "Field"
        ):
            if isinstance(node.target, ast.Name):
                field_name = node.target.id

                # Get the type annotation
                type_annotation = node.annotation

                # Determine if the type is Optional
                is_optional = (
                    isinstance(type_annotation, ast.Subscript)
                    and isinstance(type_annotation.value, ast.Name)
                    and type_annotation.value.id == "Optional"
                )

                if is_optional:
                    # Check for PF001
                    if not any(
                        kw.arg == "default" for kw in node.value.keywords
                    ):
                        self.issues.append(
                            (
                                node.lineno,
                                node.col_offset,
                                f"PF001 Field '{field_name}' should use 'default=None' for optional fields",
                                type(self),
                            )
                        )
                else:
                    # Check to see if a variable is defined as required *with* a value
                    if node.value.args:
                        first_arg = node.value.args[0]
                        if (
                            not isinstance(first_arg, ast.Constant)
                            or first_arg.value is not Ellipsis
                        ):
                            pass
                    else:
                        # No arguments provided, defaulting to required field check
                        self.issues.append(
                            (
                                node.lineno,
                                node.col_offset,
                                f"PF002 Field '{field_name}' should use '...' for required fields",
                                type(self),
                            )
                        )
        else:
            # Handle missing Field case for required fields
            if isinstance(node.target, ast.Name):
                field_name = node.target.id
                type_annotation = node.annotation

                # Determine if the type is Optional
                is_optional = (
                    isinstance(type_annotation, ast.Subscript)
                    and isinstance(type_annotation.value, ast.Name)
                    and type_annotation.value.id == "Optional"
                )

                if not is_optional:
                    self.issues.append(
                        (
                            node.lineno,
                            node.col_offset,
                            f"PF002 Field '{field_name}' should use '...' for required fields",
                            type(self),
                        )
                    )


def run_ast_checks(
    tree: ast.AST,
) -> Generator[Tuple[int, int, str, type], None, None]:
    checker = PydanticFieldChecker(tree)
    yield from checker.run()
