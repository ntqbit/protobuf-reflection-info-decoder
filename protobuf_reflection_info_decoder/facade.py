from typing import List, Tuple

from .proto_constructor import construct_proto
from .reflection_parser import parse_message_layout


def decode_to_proto(seq_obj_pairs: List[Tuple[str, list]]):
    return construct_proto([
        parse_message_layout(seq, objects)
        for seq, objects in seq_obj_pairs
    ])
