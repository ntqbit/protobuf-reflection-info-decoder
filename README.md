# Protobuf reflection info decoder
Recreates .proto message from Java message reflection info (UTF-16 sequence and Object[]).

# Install
Clone this repository and run
```bash
pip install .
```

# How to use
See [example.py](./example.py)

Result:
```
syntax = 'proto2';

message UnknownMessage1
{
	// WARNING: Unable to recover message type name.
	optional bytes field1 = 1;

	// WARNING: Unable to recover message type name.
	// Class reference: Message1
	repeated bytes field2 = 2;
	optional string versionNamePrefix_ = 3;

	// WARNING: Unable to recover enum type name.
	required JUNKENUM field3 = 4;

	oneof field0
	{
		string unknown_1 = 5;
		string unknown_2 = 10;

		// WARNING: Unable to recover message type name.
		// Class reference: Message3
		bytes unknown_3 = 11;

		// WARNING: Unable to recover enum type name.
		// EnumLiteMap: Message4
		JUNKENUM unknown_4 = 12;
	}

	optional bool field55 = 6;
	required bool field78 = 7;
	optional bool field79 = 8;
	repeated bytes field99 = 9;
	optional int32 field100 = 13;
	optional string field500 = 14;

	// WARNING: Unable to recover map types.
	map<JUNKTYPE, JUNKTYPE> myMap_ = 15;

	// WARNING: Unable to recover map types.
	map<JUNKTYPE, JUNKTYPE> mapWithEnum_ = 16;
	optional int32 unknown_ = 24;
}
```