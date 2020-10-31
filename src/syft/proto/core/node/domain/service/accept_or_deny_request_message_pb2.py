# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: proto/core/node/domain/service/accept_or_deny_request_message.proto
"""Generated protocol buffer code."""
# third party
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database

# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


# syft absolute
from syft.proto.core.common import (
    common_object_pb2 as proto_dot_core_dot_common_dot_common__object__pb2,
)
from syft.proto.core.io import address_pb2 as proto_dot_core_dot_io_dot_address__pb2

DESCRIPTOR = _descriptor.FileDescriptor(
    name="proto/core/node/domain/service/accept_or_deny_request_message.proto",
    package="syft.core.node.domain.service",
    syntax="proto3",
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
    serialized_pb=b'\nCproto/core/node/domain/service/accept_or_deny_request_message.proto\x12\x1dsyft.core.node.domain.service\x1a%proto/core/common/common_object.proto\x1a\x1bproto/core/io/address.proto"\xa6\x01\n\x1a\x41\x63\x63\x65ptOrDenyRequestMessage\x12%\n\x06msg_id\x18\x01 \x01(\x0b\x32\x15.syft.core.common.UID\x12&\n\x07\x61\x64\x64ress\x18\x02 \x01(\x0b\x32\x15.syft.core.io.Address\x12)\n\nrequest_id\x18\x03 \x01(\x0b\x32\x15.syft.core.common.UID\x12\x0e\n\x06\x61\x63\x63\x65pt\x18\x04 \x01(\x08\x62\x06proto3',
    dependencies=[
        proto_dot_core_dot_common_dot_common__object__pb2.DESCRIPTOR,
        proto_dot_core_dot_io_dot_address__pb2.DESCRIPTOR,
    ],
)


_ACCEPTORDENYREQUESTMESSAGE = _descriptor.Descriptor(
    name="AcceptOrDenyRequestMessage",
    full_name="syft.core.node.domain.service.AcceptOrDenyRequestMessage",
    filename=None,
    file=DESCRIPTOR,
    containing_type=None,
    create_key=_descriptor._internal_create_key,
    fields=[
        _descriptor.FieldDescriptor(
            name="msg_id",
            full_name="syft.core.node.domain.service.AcceptOrDenyRequestMessage.msg_id",
            index=0,
            number=1,
            type=11,
            cpp_type=10,
            label=1,
            has_default_value=False,
            default_value=None,
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
            create_key=_descriptor._internal_create_key,
        ),
        _descriptor.FieldDescriptor(
            name="address",
            full_name="syft.core.node.domain.service.AcceptOrDenyRequestMessage.address",
            index=1,
            number=2,
            type=11,
            cpp_type=10,
            label=1,
            has_default_value=False,
            default_value=None,
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
            create_key=_descriptor._internal_create_key,
        ),
        _descriptor.FieldDescriptor(
            name="request_id",
            full_name="syft.core.node.domain.service.AcceptOrDenyRequestMessage.request_id",
            index=2,
            number=3,
            type=11,
            cpp_type=10,
            label=1,
            has_default_value=False,
            default_value=None,
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
            create_key=_descriptor._internal_create_key,
        ),
        _descriptor.FieldDescriptor(
            name="accept",
            full_name="syft.core.node.domain.service.AcceptOrDenyRequestMessage.accept",
            index=3,
            number=4,
            type=8,
            cpp_type=7,
            label=1,
            has_default_value=False,
            default_value=False,
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
            create_key=_descriptor._internal_create_key,
        ),
    ],
    extensions=[],
    nested_types=[],
    enum_types=[],
    serialized_options=None,
    is_extendable=False,
    syntax="proto3",
    extension_ranges=[],
    oneofs=[],
    serialized_start=171,
    serialized_end=337,
)

_ACCEPTORDENYREQUESTMESSAGE.fields_by_name[
    "msg_id"
].message_type = proto_dot_core_dot_common_dot_common__object__pb2._UID
_ACCEPTORDENYREQUESTMESSAGE.fields_by_name[
    "address"
].message_type = proto_dot_core_dot_io_dot_address__pb2._ADDRESS
_ACCEPTORDENYREQUESTMESSAGE.fields_by_name[
    "request_id"
].message_type = proto_dot_core_dot_common_dot_common__object__pb2._UID
DESCRIPTOR.message_types_by_name[
    "AcceptOrDenyRequestMessage"
] = _ACCEPTORDENYREQUESTMESSAGE
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

AcceptOrDenyRequestMessage = _reflection.GeneratedProtocolMessageType(
    "AcceptOrDenyRequestMessage",
    (_message.Message,),
    {
        "DESCRIPTOR": _ACCEPTORDENYREQUESTMESSAGE,
        "__module__": "proto.core.node.domain.service.accept_or_deny_request_message_pb2"
        # @@protoc_insertion_point(class_scope:syft.core.node.domain.service.AcceptOrDenyRequestMessage)
    },
)
_sym_db.RegisterMessage(AcceptOrDenyRequestMessage)


# @@protoc_insertion_point(module_scope)
