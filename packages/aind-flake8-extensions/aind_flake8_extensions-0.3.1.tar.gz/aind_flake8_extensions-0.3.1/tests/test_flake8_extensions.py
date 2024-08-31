import ast
import unittest
from aind_flake8_extensions.plugin import run_ast_checks


class TestPydanticFieldChecker(unittest.TestCase):

    def check_code(self, code: str):
        """Helper method to run the PydanticFieldChecker on the provided code."""
        tree = ast.parse(code)
        return list(run_ast_checks(tree))

    def test_optional_field_missing_default(self):
        code = """
from pydantic import BaseModel, Field

class MyModel(BaseModel):
    name: Optional[str] = Field(None, description="Name of the user")
"""
        errors = self.check_code(code)
        self.assertEqual(len(errors), 1)
        self.assertEqual(errors[0][2], "PF001 Field 'name' should use 'default=None' for optional fields")

    def test_required_field_missing_ellipsis(self):
        code = """
from pydantic import BaseModel, Field

class MyModel(BaseModel):
    name: str = Field(description="Name of the user")
"""
        errors = self.check_code(code)
        self.assertEqual(len(errors), 1)
        self.assertEqual(errors[0][2], "PF002 Field 'name' should use '...' for required fields")

    def test_required_field_no_args(self):
        code = """
from pydantic import BaseModel, Field

class MyModel(BaseModel):
    name: str = Field()
"""
        errors = self.check_code(code)
        self.assertEqual(len(errors), 1)
        self.assertEqual(errors[0][2], "PF002 Field 'name' should use '...' for required fields")

    def test_required_field_blank(self):
        code = """
from pydantic import BaseModel, Field

class MyModel(BaseModel):
    name: str
"""
        errors = self.check_code(code)
        self.assertEqual(len(errors), 1)
        self.assertEqual(errors[0][2], "PF002 Field 'name' should use '...' for required fields")

    def test_correct_optional_field(self):
        code = """
from pydantic import BaseModel, Field

class MyModel(BaseModel):
    name: Optional[str] = Field(default=None, description="Name of the user")
"""
        errors = self.check_code(code)
        self.assertEqual(len(errors), 0)

    def test_correct_required_field_with_args(self):
        code = """
from pydantic import BaseModel, Field

class MyModel(BaseModel):
    name: str = Field(..., title="blank", description="Name of the user")
"""
        errors = self.check_code(code)
        self.assertEqual(len(errors), 0)

    def test_correct_required_field(self):
        code = """
from pydantic import BaseModel, Field

class MyModel(BaseModel):
    name: str = Field(...)
"""
        errors = self.check_code(code)
        self.assertEqual(len(errors), 0)

    def test_correct_required_field_args(self):
        code = """
from pydantic import BaseModel, Field

class MyModel(BaseModel):
    name: str = Field(..., description="Description")
"""
        errors = self.check_code(code)
        self.assertEqual(len(errors), 0)

    def test_no_fields(self):
        code = """
from pydantic import BaseModel

class MyModel(BaseModel):
    pass
"""
        errors = self.check_code(code)
        self.assertEqual(len(errors), 0)

    def test_correct_required_default_set(self):
        code = """
from pydantic import BaseModel

class MyModel(BaseModel):
    stimulus_devices: List[int] = Field(default=[])
"""
        errors = self.check_code(code)
        self.assertEqual(len(errors), 0)

    def test_correct_required_with_value(self):
        code = """
from pydantic import BaseModel, Field

class MyModel(BaseModel):
    name: str = Field("value")
"""
        errors = self.check_code(code)
        self.assertEqual(len(errors), 0)

    def test_correct_required_with_object(self):
        code = """
from pydantic import BaseModel, Field

class ValueModel(BaseModel):
    data: int = Field(...)

class MyModel(BaseModel):
    value: ValueModel = Field(ValueModel(int=1))
"""
        errors = self.check_code(code)
        self.assertEqual(len(errors), 0)


if __name__ == '__main__':
    unittest.main()
