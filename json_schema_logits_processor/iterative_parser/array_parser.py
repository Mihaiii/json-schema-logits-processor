from json_schema_logits_processor.iterative_parser.types import IterativeParserResult
from json_schema_logits_processor.schema.interative_schema import ArrayJsonSchema, JsonSchema, SchemaId
from json_schema_logits_processor.iterative_parser.content_parser import _parse_one_token

def is_valid_array(
    json_str: str, schema: ArrayJsonSchema, state: IterativeParserResult
) -> IterativeParserResult:
    while state.string_index < len(json_str):
        char = json_str[state.string_index]

        if char.isspace():
            state.string_index += 1
            continue

        if char == '[':
            state.string_index += 1
            state.value_stack.append('[')
            continue

        if char == ']':
            state.string_index += 1
            if state.value_stack and state.value_stack[-1] == '[':
                state.value_stack.pop()
            return IterativeParserResult(
                valid=True,
                complete=len(state.value_stack) == 0,
                string_index=state.string_index,
                schema_id=schema.parent_id,
                next_state=0,
                value_stack=state.value_stack,
            )

        if char == ',':
            state.string_index += 1
            if state.string_index >= len(json_str) or json_str[state.string_index].isspace() or json_str[state.string_index] in [']', ',']:
                return IterativeParserResult(
                    valid=False,
                    complete=False,
                    string_index=state.string_index,
                    schema_id=schema.id,
                    next_state=0,
                    value_stack=state.value_stack,
                )
            continue

        # Validate the item within the array
        item_schema = schema.items
        item_state = _parse_one_token(json_str, state, item_schema)
        if not item_state.valid:
            return item_state
        state = item_state

    return IterativeParserResult(
        valid=False,
        complete=False,
        string_index=state.string_index,
        schema_id=schema.id,
        next_state=0,
        value_stack=state.value_stack,
    )