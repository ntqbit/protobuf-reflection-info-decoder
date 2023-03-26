import argparse

from protobuf_reflection_info_decoder import decode_to_proto

parser = argparse.ArgumentParser()
parser.add_argument('--output', '-o', type=str, help='Path to output .proto file')
args = parser.parse_args()

output_file = args.output or 'output.proto'

seq = "\u0001\u0011\u0001\u0001\u0001\u0018\u0011\u0002\u0002\u0002\u0001\u1009\u0000\u0002" +\
    "\u001b\u0003\u1008\u0005\u0004\u150c\u0007\u0005\u103b\u0000\u0006\u1007\u0006\u0007" +\
    "\u1507\b\b\u1007\t\t\u001c\n\u103b\u0000\u000b\u103c\u0000\f\u103f\u0000\r\u1004" +\
    "\n\u000e\u1008\u000b\u000f2\u0010\u0832\u0018\u1004\f"

objects = [
    "field0",
    "field0Case",
    "bitField0_",
    "field1",
    "field2",
    "Message1",
    "versionNamePrefix_",
    "field3",
    "Message2",
    "field55",
    "field78",
    "field79",
    "field99",
    "Message3",
    "Message4",
    "field100",
    "field500",
    "myMap_",
    "MyMapDefaultEntryHolder.defaultEntry",
    "mapWithEnum_",
    "MapWithEnumDefaultEntryHolder.defaultEntry",
    "Message5",
    "unknown_"
]

proto_file = decode_to_proto([(seq, objects)])
with open(output_file, 'w') as f:
    f.write(proto_file)

print('[+] Done!')
