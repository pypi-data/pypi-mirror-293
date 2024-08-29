import os
import sys
from array import array
from io import BytesIO
from pathlib import Path
from shutil import which

import pytest
import requests

from proto_topy import (
    CompilationFailed,
    DelimitedMessageFactory,
    ProtoCollection,
    ProtoModule,
)

protoc_path = Path(which("protoc") or os.environ.get("PROTOC"))


@pytest.fixture()
def address_book():
    return requests.get(
        "https://raw.githubusercontent.com/protocolbuffers/protobuf/main/examples/addressbook.proto"
    ).text


def test_compiler_version():
    version = ProtoCollection().compiler_version(compiler_path=protoc_path)
    assert version is not None and tuple(map(int, version.split("."))) > (3, 0, 0)


def unlink_proto_file(path_str: str) -> Path:
    proto_path = Path(path_str)
    if proto_path.exists():
        proto_path.unlink()
    return proto_path


def test_add_proto():
    test1_proto = unlink_proto_file("test1.proto")
    proto = ProtoModule(file_path=test1_proto, source="")
    modules = ProtoCollection()
    modules.add_proto(proto)
    assert test1_proto in modules.modules
    unlink_proto_file("test1.proto")


def test_add_proto2():
    test2_proto = unlink_proto_file("test2.proto")
    test3_proto = unlink_proto_file("test3.proto")

    modules = ProtoCollection(
        *(
            ProtoModule(file_path=test2_proto, source=""),
            ProtoModule(file_path=test3_proto, source=""),
        )
    )
    assert test2_proto in modules.modules
    assert test3_proto in modules.modules
    unlink_proto_file("test2.proto")
    unlink_proto_file("test3.proto")


def test_bad_protoc():
    dummy = unlink_proto_file("dummy")
    with pytest.raises(FileNotFoundError):
        ProtoCollection().compiled(compiler_path=dummy)
    unlink_proto_file("dummy")


def test_compile_invalid_source():
    test4_proto = unlink_proto_file("test4.proto")
    with pytest.raises(CompilationFailed):
        ProtoModule(file_path=test4_proto, source="foo").compiled(
            compiler_path=protoc_path
        )
    unlink_proto_file("test4.proto")


def test_compile_redundant_proto():
    testr_proto = unlink_proto_file("testr.proto")
    proto_source = 'syntax = "proto3"; message TestR { int32 foo = 1; };'
    proto1 = ProtoModule(file_path=testr_proto, source=proto_source)
    proto2 = ProtoModule(file_path=testr_proto, source=proto_source)
    with pytest.raises(KeyError, match=r"testr.proto already added"):
        ProtoCollection(proto1, proto2).compiled(compiler_path=protoc_path)
    unlink_proto_file("testr.proto")


def test_compile_minimal_proto():
    from google.protobuf.timestamp_pb2 import Timestamp

    test5_proto = unlink_proto_file("test5.proto")
    proto = ProtoModule(
        file_path=test5_proto,
        source="""
    syntax = "proto3";
    import "google/protobuf/timestamp.proto";
    message Test5 {
        google.protobuf.Timestamp created = 1;
    }
    """,
    ).compiled(protoc_path)
    sys.modules["test5"] = proto.py
    atest5 = proto.py.Test5()
    assert isinstance(atest5.created, Timestamp)
    del sys.modules["test5"]
    unlink_proto_file("test5.proto")


def test_compile_minimal_proto_in_a_package():
    from google.protobuf.timestamp_pb2 import Timestamp

    thing_proto = unlink_proto_file("p1/p2/p3/thing.proto")
    proto = ProtoModule(
        file_path=thing_proto,
        source="""
    syntax = "proto3";
    import "google/protobuf/timestamp.proto";
    message Thing {
        google.protobuf.Timestamp created = 1;
    }
    """,
    ).compiled(protoc_path)
    assert "# source: p1/p2/p3/thing.proto" in proto.py_source.split("\n")
    sys.modules["thing"] = proto.py
    athing = proto.py.Thing()
    assert isinstance(athing.created, Timestamp)
    unlink_proto_file("p1/p2/p3/thing.proto")


def test_compile_missing_dependency():
    test_proto = unlink_proto_file("test.proto")
    with pytest.raises(CompilationFailed, match=r"other.proto: File not found.*"):
        ProtoModule(
            file_path=test_proto,
            source='syntax = "proto3"; import "other.proto";',
        ).compiled(protoc_path)
    unlink_proto_file("test.proto")


def test_compile_ununsed_dependency():
    test_proto = unlink_proto_file("test.proto")
    proto_module = ProtoModule(
        file_path=test_proto,
        source="""
    syntax = "proto3";
    import "other.proto";
    """,
    )

    other_proto = unlink_proto_file("other.proto")
    other_proto_module = ProtoModule(
        file_path=other_proto,
        source="""
    syntax = "proto3";
    import "google/protobuf/timestamp.proto";
    message OtherThing {
        google.protobuf.Timestamp created = 1;
    }
    """,
    )
    modules = ProtoCollection(proto_module, other_proto_module)
    try:
        modules.compiled(compiler_path=protoc_path)
    except CompilationFailed:
        pytest.fail("Unexpected CompilationFailed ..")
    unlink_proto_file("test.proto")
    unlink_proto_file("other.proto")


def test_compile_simple_dependency():
    from google.protobuf.timestamp_pb2 import Timestamp

    test_proto = unlink_proto_file("p3/p4/test6.proto")
    proto_module = ProtoModule(
        file_path=test_proto,
        source="""
    syntax = "proto3";
    import "p1/p2/other2.proto";
    message Test6 {
        OtherThing2 foo = 1;
    };
    """,
    )

    other_proto = unlink_proto_file("p1/p2/other2.proto")
    other_proto_module = ProtoModule(
        file_path=other_proto,
        source="""
    syntax = "proto3";
    import "google/protobuf/timestamp.proto";
    message OtherThing2 {
        google.protobuf.Timestamp created = 1;
    }
    """,
    )
    modules = ProtoCollection(proto_module, other_proto_module)
    modules.compiled(compiler_path=protoc_path)
    sys.modules.update({proto.name: proto.py for proto in modules.modules.values()})
    atest6 = modules.modules[test_proto].py.Test6()
    assert isinstance(atest6.foo.created, Timestamp)
    for proto_module in modules.modules.values():
        del sys.modules[proto_module.name]
    unlink_proto_file("p3/p4/test6.proto")
    unlink_proto_file("p1/p2/other2.proto")


def test_encode_message():
    proto_source = 'syntax = "proto3"; message Test{n} {{ int32 foo = 1; }};'
    test7_proto = unlink_proto_file("test7.proto")
    test8_proto = unlink_proto_file("test8.proto")

    proto1 = ProtoModule(file_path=test7_proto, source=proto_source.format(n=7))
    proto2 = ProtoModule(file_path=test8_proto, source=proto_source.format(n=8))

    ProtoCollection(proto1, proto2).compiled(compiler_path=protoc_path)
    assert array("B", proto1.py.Test7(foo=124).SerializeToString()) == array(
        "B", [8, 124]
    )
    assert array("B", proto2.py.Test8(foo=123).SerializeToString()) == array(
        "B", [8, 123]
    )
    unlink_proto_file("test7.proto")
    unlink_proto_file("test8.proto")


def test_decode_message():
    test9_proto = unlink_proto_file("test9.proto")
    proto = ProtoModule(
        file_path=test9_proto,
        source='syntax = "proto3"; message Test9 { int32 foo = 1; };',
    ).compiled(protoc_path)
    aTest9 = proto.py.Test9()
    aTest9.ParseFromString(bytes(array("B", [8, 124])))
    assert aTest9.foo == 124
    unlink_proto_file("test9.proto")


def test_decode_messages_stream():
    test10_proto = unlink_proto_file("test10.proto")
    proto = ProtoModule(
        file_path=test10_proto,
        source='syntax = "proto3"; message Test10 { int32 foo = 1; };',
    ).compiled(protoc_path)
    factory = DelimitedMessageFactory(
        BytesIO(), *(proto.py.Test10(foo=foo) for foo in [1, 12])
    )
    factory.stream.seek(0)
    assert [thing.foo for _, thing in factory.message_read(proto.py.Test10)] == [1, 12]
    unlink_proto_file("test10.proto")


def test_decode_messages_stream2():
    test11_proto = unlink_proto_file("test11.proto")
    proto = ProtoModule(
        file_path=test11_proto,
        source='syntax = "proto3"; message Test11 { int32 foo = 1; };',
    ).compiled(protoc_path)
    message = DelimitedMessageFactory(
        BytesIO(), *(proto.py.Test11(foo=foo) for foo in [1, 12])
    )

    for fn in message.read, message.bytes_read:
        message.stream.seek(0)
        foos = []
        for offset_data in fn():
            aTest11 = proto.py.Test11()
            aTest11.ParseFromString(offset_data[1])
            foos.append(aTest11.foo)
        assert foos == [1, 12]
    unlink_proto_file("test11.proto")


@pytest.mark.vcr
def test_google_addressbook_example(address_book):

    adressbook_proto = unlink_proto_file(
        "protocolbuffers/protobuf/blob/main/examples/addressbook.proto"
    )
    proto = ProtoModule(
        file_path=adressbook_proto,
        source=address_book,
    ).compiled(protoc_path)
    sys.modules["addressbook"] = proto.py

    # Produce serialized address book
    address_book = proto.py.AddressBook()
    person = address_book.people.add()
    person.id = 111
    person.name = "A Name"
    person.email = "a.name@mail.com"
    phone_number = person.phones.add()
    phone_number.number = "+1234567"
    phone_number.type = proto.py.Person.MOBILE
    address_book_data = address_book.SerializeToString()

    # Read address book
    address_book = proto.py.AddressBook()
    address_book.ParseFromString(address_book_data)
    person = address_book.people[0]
    assert person.id == 111
    assert person.name == "A Name"
    assert person.email == "a.name@mail.com"
    assert phone_number.number == "+1234567"
    assert phone_number.type == proto.py.Person.MOBILE
