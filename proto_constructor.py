from typing import List
from layout import FieldLayout, MessageLayout, Syntax,\
    FieldCollection, FieldTypes, FIELDS_COLLECTIONS

JUNKTYPE = 'JUNKTYPE'
JUNKENUM = 'JUNKENUM'


class Printer:
    def new_line(self, count=1):
        raise NotImplementedError

    def println(self, line):
        return self.printlines([line])

    def printlines(self, lines):
        raise NotImplementedError


def is_field_list(field_type: FieldTypes):
    return FIELDS_COLLECTIONS[field_type] in [FieldCollection.VECTOR, FieldCollection.PACKED_VECTOR]


def is_field_packed(field_type: FieldTypes):
    return FIELDS_COLLECTIONS[field_type] == FieldCollection.PACKED_VECTOR


def get_field_label(syntax: Syntax, field: FieldLayout):
    if is_field_list(field.type):
        return 'repeated'

    if FIELDS_COLLECTIONS[field.type] == FieldCollection.MAP:
        return ''

    if syntax == Syntax.PROTO2:
        return 'required' if field.required else 'optional'

    return ''

    # FieldTypes.MESSAGE: 'message',
    # FieldTypes.GROUP: 'group',
    # FieldTypes.MESSAGE_LIST: 'message',
    # FieldTypes.GROUP_LIST: 'group',

    # FieldTypes.ENUM: 'enum',
    # FieldTypes.ENUM_LIST: 'enum',
    # FieldTypes.ENUM_LIST_PACKED: 'enum',

    # FieldTypes.MAP: 'map',

    # oneof


ENUM_TYPES = [FieldTypes.ENUM, FieldTypes.ENUM_LIST, FieldTypes.BOOL_LIST_PACKED]
MESSAGE_TYPES = [FieldTypes.MESSAGE, FieldTypes.GROUP, FieldTypes.MESSAGE_LIST, FieldTypes.GROUP_LIST]

PRIMITIVE_FIELD_TYPE_NAMES = {
    FieldTypes.DOUBLE: 'double',
    FieldTypes.FLOAT: 'float',
    FieldTypes.INT64: 'int64',
    FieldTypes.UINT64: 'uint64',
    FieldTypes.INT32: 'int32',
    FieldTypes.FIXED64: 'fixed64',
    FieldTypes.FIXED32: 'fixed32',
    FieldTypes.BOOL: 'bool',
    FieldTypes.STRING: 'string',
    FieldTypes.BYTES: 'bytes',
    FieldTypes.UINT32: 'uint32',
    FieldTypes.SFIXED32: 'sfixed32',
    FieldTypes.SFIXED64: 'sfixed64',
    FieldTypes.SINT32: 'sint32',
    FieldTypes.SINT64: 'sint64',
    FieldTypes.DOUBLE_LIST: 'double',
    FieldTypes.FLOAT_LIST: 'float',
    FieldTypes.INT64_LIST: 'int64',
    FieldTypes.UINT64_LIST: 'uint64',
    FieldTypes.INT32_LIST: 'int32',
    FieldTypes.FIXED64_LIST: 'fixed64',
    FieldTypes.FIXED32_LIST: 'fixed32',
    FieldTypes.BOOL_LIST: 'bool',
    FieldTypes.STRING_LIST: 'string',
    FieldTypes.BYTES_LIST: 'bytes',
    FieldTypes.UINT32_LIST: 'uint32',
    FieldTypes.SFIXED32_LIST: 'sfixed32',
    FieldTypes.SFIXED64_LIST: 'sfixed64',
    FieldTypes.SINT32_LIST: 'sint32',
    FieldTypes.SINT64_LIST: 'sint64',
    FieldTypes.DOUBLE_LIST_PACKED: 'double',
    FieldTypes.FLOAT_LIST_PACKED: 'float',
    FieldTypes.INT64_LIST_PACKED: 'int64',
    FieldTypes.UINT64_LIST_PACKED: 'uint64',
    FieldTypes.INT32_LIST_PACKED: 'int32',
    FieldTypes.FIXED64_LIST_PACKED: 'fixed64',
    FieldTypes.FIXED32_LIST_PACKED: 'fixed32',
    FieldTypes.BOOL_LIST_PACKED: 'bool',
    FieldTypes.UINT32_LIST_PACKED: 'uint32',
    FieldTypes.SFIXED32_LIST_PACKED: 'sfixed32',
    FieldTypes.SFIXED64_LIST_PACKED: 'sfixed64',
    FieldTypes.SINT32_LIST_PACKED: 'sint32',
    FieldTypes.SINT64_LIST_PACKED: 'sint64',
}


class IndentedPrinter(Printer):
    def __init__(self, printer: Printer):
        self._printer = printer

        self._indentation = 0

    def increase_indent(self, indent=1):
        self._indentation += indent

    def decrease_indent(self, indent=1):
        if indent > self._indentation:
            raise ValueError('Indentation can not be decreased to negative value')

        self._indentation -= indent

    def new_line(self, count=1):
        return self._printer.new_line(count)

    def println(self, line):
        return self._printer.println(self._indent_line(line))

    def printlines(self, lines):
        indented_lines = [self._indent_line(line) for line in lines]
        return self._printer.printlines(indented_lines)

    def _indent_line(self, line):
        return self._get_indent() + line

    def _get_indent(self):
        return '\t' * self._indentation


class UniqueNameGenerator:
    def __init__(self, prefix, start=1):
        self._prefix = prefix
        self._counter = start

    def generate(self):
        name = self._prefix + str(self._counter)
        self._counter += 1
        return name


class Statement:
    def __init__(self, printer: IndentedPrinter, statement_type, name):
        self._printer = printer
        self._type = statement_type
        self._name = name

    def __enter__(self):
        self.enter()

    def __exit__(self, exc_type, exc_value, traceback):
        self.exit()

    def enter(self):
        self._printer.println(f'{self._type} {self._name}')
        self._printer.println('{')
        self._printer.increase_indent()

    def exit(self):
        self._printer.decrease_indent()
        self._printer.println('}')
        self._printer.new_line()


class ProtoConstructor:
    def __init__(self, printer: Printer):
        self._printer = IndentedPrinter(printer)

        self._last_syntax: Syntax = None
        self._message_name_generator = UniqueNameGenerator('UnknownMessage')

    def add_message(self, message: MessageLayout, message_name: str = None):
        self.newline()
        self.ensure_last_syntax(message.syntax)

        with self._create_message_statement(self._get_message_name(message_name)):
            field_name_generator = UniqueNameGenerator('unknown_')

            # Group oneof fields into a single list
            fields = []
            oneof_groups = {}

            for field in message.fields:
                if field.is_oneof:
                    if field.oneof_value_reference in oneof_groups:
                        oneof_groups[field.oneof_value_reference].append(field)
                    else:
                        oneof_group = [field]
                        fields.append(oneof_group)
                        oneof_groups[field.oneof_value_reference] = oneof_group
                else:
                    fields.append(field)

            # Add fields and oneofs
            for i, field in enumerate(fields):
                if isinstance(field, list):
                    self._add_oneof(i, message.syntax, field, field_name_generator)
                else:
                    self._add_field(i, False, message.syntax, field, field_name_generator)

    def _create_message_statement(self, message_name: str):
        return Statement(self._printer, 'message', message_name)

    def _add_oneof(self, field_idx: int, syntax: Syntax,
                   oneof_fields: List[FieldLayout], field_name_generator: UniqueNameGenerator):
        self.newline()

        with self._create_oneof_statement(oneof_fields[0].oneof_value_reference):
            for i, field in enumerate(oneof_fields):
                self._add_field(i, True, syntax, field, field_name_generator)

    def _create_oneof_statement(self, oneof_name: str):
        return Statement(self._printer, 'oneof', oneof_name)

    def _add_field(self, field_idx: int, oneof: bool, syntax: Syntax,
                   field: FieldLayout, field_name_generator: UniqueNameGenerator):
        words = []

        # Get field label
        if not oneof:
            field_label = get_field_label(syntax, field)
            if field_label:
                words.append(field_label)

        # Get field type name and add comment if needed
        comment = []

        if field.type in PRIMITIVE_FIELD_TYPE_NAMES:
            field_type_name = PRIMITIVE_FIELD_TYPE_NAMES[field.type]
        elif field.type in ENUM_TYPES:
            comment = ['WARNING: Unable to recover enum type name.']
            if field.enum_lite_map:
                comment.append('EnumLiteMap: ' + field.enum_lite_map)
            field_type_name = 'JUNKENUM'
        elif field.type in MESSAGE_TYPES:
            comment = ['WARNING: Unable to recover message type name.']
            if field.class_reference:
                comment.append('Class reference: ' + field.class_reference)
            field_type_name = PRIMITIVE_FIELD_TYPE_NAMES[FieldTypes.BYTES]
        elif field.type == FieldTypes.MAP:
            comment = ['WARNING: Unable to recover map types.']
            field_type_name = f'map<{JUNKTYPE}, {JUNKTYPE}>'

        # Add other words
        field_name = self._get_field_name(field_name_generator, field.field_reference)
        words += [field_type_name, field_name, '=', str(field.number)]

        if is_field_packed(field.type):
            words.append(' [packed = true]')

        # Compose words into field line
        field_line = ' '.join(words) + ';'

        # Print comment
        if comment:
            if field_idx != 0:
                self.newline()

            for line in comment:
                self.print_comment(line)

        # Print field line
        self.println(field_line)

    def _get_field_name(self, generator: UniqueNameGenerator, field_reference: str = None):
        if field_reference:
            return str(field_reference)

        return generator.generate()

    def _get_message_name(self, message_name: str = None):
        if message_name:
            return message_name

        return self._message_name_generator.generate()

    def ensure_last_syntax(self, syntax: Syntax):
        if self._last_syntax == syntax:
            return

        self._last_syntax = syntax
        self.print_syntax(syntax)

    def print_syntax(self, syntax: Syntax):
        syntax_name = 'proto3' if syntax == Syntax.PROTO3 else 'proto2'
        self.println(f"syntax = '{syntax_name}';")
        self.newline()

    def newline(self):
        self._printer.new_line()

    def print_multiline_comment(self, comment_lines):
        self._printer.printlines([
            '\\*',
            *[' * ' + line for line in comment_lines],
            ' */'
        ])

    def print_comment(self, comment):
        self._printer.println('// ' + comment)

    def println(self, line):
        self._printer.println(line)

    def up(self):
        self._printer.increase_indent()

    def down(self):
        self._printer.decrease_indent()


class TextPrinter(Printer):
    def __init__(self):
        self._lines = []

    def new_line(self, count=1):
        self._lines += [''] * count

    def printlines(self, lines):
        self._lines += lines

    def get_text(self):
        return '\n'.join(self._lines)


def construct_proto(messages: List[MessageLayout]):
    printer = TextPrinter()
    constructor = ProtoConstructor(printer)
    for message in messages:
        constructor.add_message(message)
    return printer.get_text()
