from enum import Enum
from typing import List

ONEOF_TYPE_OFFSET = 51


class FieldCollection(Enum):
    SCALAR = 1
    VECTOR = 2
    PACKED_VECTOR = 3
    MAP = 4


class FieldTypes(Enum):
    DOUBLE = 0
    FLOAT = 1
    INT64 = 2
    UINT64 = 3
    INT32 = 4
    FIXED64 = 5
    FIXED32 = 6
    BOOL = 7
    STRING = 8
    MESSAGE = 9
    BYTES = 10
    UINT32 = 11
    ENUM = 12
    SFIXED32 = 13
    SFIXED64 = 14
    SINT32 = 15
    SINT64 = 16
    GROUP = 17
    DOUBLE_LIST = 18
    FLOAT_LIST = 19
    INT64_LIST = 20
    UINT64_LIST = 21
    INT32_LIST = 22
    FIXED64_LIST = 23
    FIXED32_LIST = 24
    BOOL_LIST = 25
    STRING_LIST = 26
    MESSAGE_LIST = 27
    BYTES_LIST = 28
    UINT32_LIST = 29
    ENUM_LIST = 30
    SFIXED32_LIST = 31
    SFIXED64_LIST = 32
    SINT32_LIST = 33
    SINT64_LIST = 34
    DOUBLE_LIST_PACKED = 35
    FLOAT_LIST_PACKED = 36
    INT64_LIST_PACKED = 37
    UINT64_LIST_PACKED = 38
    INT32_LIST_PACKED = 39
    FIXED64_LIST_PACKED = 40
    FIXED32_LIST_PACKED = 41
    BOOL_LIST_PACKED = 42
    UINT32_LIST_PACKED = 43
    ENUM_LIST_PACKED = 44
    SFIXED32_LIST_PACKED = 45
    SFIXED64_LIST_PACKED = 46
    SINT32_LIST_PACKED = 47
    SINT64_LIST_PACKED = 48
    GROUP_LIST = 49
    MAP = 50


FIELDS_COLLECTIONS = {
    FieldTypes.DOUBLE: FieldCollection.SCALAR,
    FieldTypes.FLOAT: FieldCollection.SCALAR,
    FieldTypes.INT64: FieldCollection.SCALAR,
    FieldTypes.UINT64: FieldCollection.SCALAR,
    FieldTypes.INT32: FieldCollection.SCALAR,
    FieldTypes.FIXED64: FieldCollection.SCALAR,
    FieldTypes.FIXED32: FieldCollection.SCALAR,
    FieldTypes.BOOL: FieldCollection.SCALAR,
    FieldTypes.STRING: FieldCollection.SCALAR,
    FieldTypes.MESSAGE: FieldCollection.SCALAR,
    FieldTypes.BYTES: FieldCollection.SCALAR,
    FieldTypes.UINT32: FieldCollection.SCALAR,
    FieldTypes.ENUM: FieldCollection.SCALAR,
    FieldTypes.SFIXED32: FieldCollection.SCALAR,
    FieldTypes.SFIXED64: FieldCollection.SCALAR,
    FieldTypes.SINT32: FieldCollection.SCALAR,
    FieldTypes.SINT64: FieldCollection.SCALAR,
    FieldTypes.GROUP: FieldCollection.SCALAR,
    FieldTypes.DOUBLE_LIST: FieldCollection.VECTOR,
    FieldTypes.FLOAT_LIST: FieldCollection.VECTOR,
    FieldTypes.INT64_LIST: FieldCollection.VECTOR,
    FieldTypes.UINT64_LIST: FieldCollection.VECTOR,
    FieldTypes.INT32_LIST: FieldCollection.VECTOR,
    FieldTypes.FIXED64_LIST: FieldCollection.VECTOR,
    FieldTypes.FIXED32_LIST: FieldCollection.VECTOR,
    FieldTypes.BOOL_LIST: FieldCollection.VECTOR,
    FieldTypes.STRING_LIST: FieldCollection.VECTOR,
    FieldTypes.MESSAGE_LIST: FieldCollection.VECTOR,
    FieldTypes.BYTES_LIST: FieldCollection.VECTOR,
    FieldTypes.UINT32_LIST: FieldCollection.VECTOR,
    FieldTypes.ENUM_LIST: FieldCollection.VECTOR,
    FieldTypes.SFIXED32_LIST: FieldCollection.VECTOR,
    FieldTypes.SFIXED64_LIST: FieldCollection.VECTOR,
    FieldTypes.SINT32_LIST: FieldCollection.VECTOR,
    FieldTypes.SINT64_LIST: FieldCollection.VECTOR,
    FieldTypes.DOUBLE_LIST_PACKED: FieldCollection.PACKED_VECTOR,
    FieldTypes.FLOAT_LIST_PACKED: FieldCollection.PACKED_VECTOR,
    FieldTypes.INT64_LIST_PACKED: FieldCollection.PACKED_VECTOR,
    FieldTypes.UINT64_LIST_PACKED: FieldCollection.PACKED_VECTOR,
    FieldTypes.INT32_LIST_PACKED: FieldCollection.PACKED_VECTOR,
    FieldTypes.FIXED64_LIST_PACKED: FieldCollection.PACKED_VECTOR,
    FieldTypes.FIXED32_LIST_PACKED: FieldCollection.PACKED_VECTOR,
    FieldTypes.BOOL_LIST_PACKED: FieldCollection.PACKED_VECTOR,
    FieldTypes.UINT32_LIST_PACKED: FieldCollection.PACKED_VECTOR,
    FieldTypes.ENUM_LIST_PACKED: FieldCollection.PACKED_VECTOR,
    FieldTypes.SFIXED32_LIST_PACKED: FieldCollection.PACKED_VECTOR,
    FieldTypes.SFIXED64_LIST_PACKED: FieldCollection.PACKED_VECTOR,
    FieldTypes.SINT32_LIST_PACKED: FieldCollection.PACKED_VECTOR,
    FieldTypes.SINT64_LIST_PACKED: FieldCollection.PACKED_VECTOR,
    FieldTypes.GROUP_LIST: FieldCollection.VECTOR,
    FieldTypes.MAP: FieldCollection.MAP
}


class FieldLayout:
    def __init__(self):
        self.number = 0
        self.type = 0
        self.required = False
        self.check_utf8 = False
        self.check_initialized = False
        self.map_proto2_enum = False
        self.supports_presence_checking = False
        self.is_oneof = False
        self.hasbits_reference = None
        self.bitfield_offset = None
        self.field_reference = None
        self.class_reference = None
        self.oneof_value_reference = None
        self.oneof_case_reference = None
        self.enum_lite_map = None
        self.map_entry = None


class Syntax(Enum):
    PROTO2 = 2
    PROTO3 = 3


class MessageLayout:
    def __init__(self):
        self.syntax = None
        self.is_message = False
        self.field_count = 0
        self.oneof_count = 0
        self.hasbits_count = 0
        self.min_field_number = 0
        self.max_field_number = 0
        self.num_entries = 0
        self.map_field_count = 0
        self.repeated_field_count = 0
        self.check_initialized_count = 0
        self.fields: List[FieldLayout] = []
