import pytest
from json_schema_logits_processor.iterative_parser.array_parser import is_valid_array
from json_schema_logits_processor.iterative_parser.types import IterativeParserResult
from json_schema_logits_processor.schema.interative_schema import ArrayJsonSchema, SchemaId, JsonSchemaParser

@pytest.fixture
def array_schema() -> ArrayJsonSchema:
    schema_str = '{"type": "array", "items": {"type": "string"}}'
    schema = JsonSchemaParser.parse_schema_from_dict(schema_str)
    array_schema = schema[SchemaId(0)]
    assert isinstance(array_schema, ArrayJsonSchema)
    return array_schema

@pytest.fixture
def start_state() -> IterativeParserResult:
    return IterativeParserResult(
        valid=True,
        complete=False,
        string_index=0,
        schema_id=SchemaId(0),
        value_stack=(),
        next_state=0,
    )

def test_empty_array(array_schema: ArrayJsonSchema, start_state: IterativeParserResult):
    json_str = "[]"
    result = is_valid_array(json_str, array_schema, start_state)
    assert result.valid
    assert result.complete
    assert result.string_index == 2

def test_single_item_array(array_schema: ArrayJsonSchema, start_state: IterativeParserResult):
    json_str = '["item"]'
    result = is_valid_array(json_str, array_schema, start_state)
    assert result.valid
    assert result.complete
    assert result.string_index == 8

def test_multiple_items_array(array_schema: ArrayJsonSchema, start_state: IterativeParserResult):
    json_str = '["item1", "item2"]'
    result = is_valid_array(json_str, array_schema, start_state)
    assert result.valid
    assert result.complete
    assert result.string_index == 17

def test_nested_array():
    schema_str = '{"type": "array", "items": {"type": "array", "items": {"type": "string"}}}'
    schema = JsonSchemaParser.parse_schema_from_dict(schema_str)
    array_schema = schema[SchemaId(0)]

    json_str = '[["item1"], ["item2"]]'
    state = IterativeParserResult(
        valid=True,
        complete=False,
        string_index=0,
        schema_id=SchemaId(0),
        next_state=0,
        value_stack=[]
    )
    result = is_valid_array(json_str, array_schema, state)
    assert result.valid
    assert result.complete
    assert result.string_index == 20

def test_invalid_array(array_schema: ArrayJsonSchema, start_state: IterativeParserResult):
    json_str = '["item1", 123]'
    result = is_valid_array(json_str, array_schema, start_state)
    assert not result.valid