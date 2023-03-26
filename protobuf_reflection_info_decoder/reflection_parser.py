from typing import List
from .layout import FieldTypes, ONEOF_TYPE_OFFSET, FieldLayout, MessageLayout, Syntax


class ParserException(Exception):
    pass


def _parse_utf16_integers(seq: str) -> List[int]:
    integers = []
    shift = 0
    integer = 0
    n = 0

    for s in map(ord, seq):
        if s < 0xD800:
            integers.append(integer | (s << shift))
            shift, integer, n = 0, 0, 0
        else:
            if s < 0xDFFF:
                raise ParserException('Unknown message format: invalid character range')

            if n == 2:
                raise ParserException('Unknown message format: character sequence longer than 3 bytes')

            integer |= (s & 0x1FFF) << shift
            shift += 13
            n += 1

    if n != 0:
        raise ParserException('Unknown message format: excess data left')

    return integers


def _parse_field_layout(is_proto2: bool, oneof_count: int, objects: list, integers_it: iter, field_objects: iter) -> FieldLayout:
    field = FieldLayout()
    field.number = next(integers_it)

    field_type_and_flags = next(integers_it)

    # Extract field information
    field_type = field_type_and_flags & 0xFF
    field.required = (field_type_and_flags & 0x100) != 0
    field.check_utf8 = (field_type_and_flags & 0x200) != 0
    field.check_initialized = (field_type_and_flags & 0x400) != 0
    field.map_proto2_enum = (field_type_and_flags & 0x800) != 0
    field.supports_presence_checking = (field_type_and_flags & 0x1000) != 0

    field.is_oneof = field_type >= ONEOF_TYPE_OFFSET

    if field.is_oneof:
        # Parse oneof field
        field_type = field_type - ONEOF_TYPE_OFFSET
        oneof_index = next(integers_it)

        field.oneof_value_reference = objects[oneof_index * 2]
        field.oneof_case_reference = objects[oneof_index * 2 + 1]

        if field_type in [FieldTypes.MESSAGE.value, FieldTypes.GROUP.value]:
            field.class_reference = next(field_objects)
        elif field_type == FieldTypes.ENUM.value and is_proto2:
            field.enum_lite_map = next(field_objects)
    else:
        # Parse non-oneof field
        field.field_reference = next(field_objects)

        # Extract field class reference, map entry, enum lite map depending on field type
        if field_type in [FieldTypes.MESSAGE_LIST.value, FieldTypes.GROUP_LIST.value]:
            field.class_reference = next(field_objects)
        elif field_type in [FieldTypes.ENUM.value, FieldTypes.ENUM_LIST.value, FieldTypes.ENUM_LIST_PACKED.value]:
            if is_proto2:
                field.class_reference = next(field_objects)
        elif field_type == FieldTypes.MAP.value:
            field.map_entry = next(field_objects)
            if field.map_proto2_enum:
                field.enum_lite_map = next(field_objects)

        # Extract hasbits object and bitfield offset
        if field.supports_presence_checking and field_type <= FieldTypes.GROUP.value:
            field_offset = next(integers_it)
            field.hasbits_reference = objects[oneof_count * 2 + field_offset // 32]
            field.bitfield_offset = field_offset % 32

    field.type = FieldTypes(field_type)
    return field


def _parse_message_layout(integers: List[int], objects: list) -> MessageLayout:
    try:
        message = MessageLayout()
        integers_it = iter(integers)

        message_flags = next(integers_it)
        is_proto2 = (message_flags & 1) != 0
        message.syntax = Syntax.PROTO2 if is_proto2 else Syntax.PROTO3
        message.is_message = (message_flags & 2) != 0
        message.field_count = next(integers_it)

        # Read message information
        if message.field_count != 0:
            message.oneof_count = next(integers_it)
            message.hasbits_count = next(integers_it)
            message.min_field_number = next(integers_it)
            message.max_field_number = next(integers_it)
            message.num_entries = next(integers_it)
            message.map_field_count = next(integers_it)
            message.repeated_field_count = next(integers_it)
            message.check_initialized_count = next(integers_it)

        # Read fields
        field_objects = iter(objects[message.oneof_count * 2 + message.hasbits_count:])

        for _ in range(message.field_count):
            message.fields.append(_parse_field_layout(is_proto2, message.oneof_count, objects, integers_it, field_objects))\

        return message
    except StopIteration:
        raise ParserException('Invalid message format')


def parse_message_layout(seq: str, objects: list):
    return _parse_message_layout(_parse_utf16_integers(seq), objects)
