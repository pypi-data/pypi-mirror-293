"""
@generated by mypy-protobuf.  Do not edit manually!
isort:skip_file
*!
Copyright (c) Streamlit Inc. (2018-2022) Snowflake Inc. (2022-2024)

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

import builtins
import google.protobuf.descriptor
import google.protobuf.message
import streamlit.proto.ArrowNamedDataSet_pb2
import streamlit.proto.Block_pb2
import streamlit.proto.Element_pb2
import streamlit.proto.NamedDataSet_pb2
import typing

DESCRIPTOR: google.protobuf.descriptor.FileDescriptor

@typing.final
class Delta(google.protobuf.message.Message):
    """A change to an element."""

    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    NEW_ELEMENT_FIELD_NUMBER: builtins.int
    ADD_BLOCK_FIELD_NUMBER: builtins.int
    ADD_ROWS_FIELD_NUMBER: builtins.int
    ARROW_ADD_ROWS_FIELD_NUMBER: builtins.int
    FRAGMENT_ID_FIELD_NUMBER: builtins.int
    fragment_id: builtins.str
    @property
    def new_element(self) -> streamlit.proto.Element_pb2.Element:
        """Append a new element to the frontend."""

    @property
    def add_block(self) -> streamlit.proto.Block_pb2.Block:
        """Append a new block to the frontend."""

    @property
    def add_rows(self) -> streamlit.proto.NamedDataSet_pb2.NamedDataSet:
        """Append data to a DataFrame in for current element. The element to add to
        is identified by the ID field, above. The dataframe is identified either
        by NamedDataSet.name or by setting NamedDataSet.has_name to false.
        All elements that contain a DataFrame should support add_rows.
        """

    @property
    def arrow_add_rows(self) -> streamlit.proto.ArrowNamedDataSet_pb2.ArrowNamedDataSet: ...
    def __init__(
        self,
        *,
        new_element: streamlit.proto.Element_pb2.Element | None = ...,
        add_block: streamlit.proto.Block_pb2.Block | None = ...,
        add_rows: streamlit.proto.NamedDataSet_pb2.NamedDataSet | None = ...,
        arrow_add_rows: streamlit.proto.ArrowNamedDataSet_pb2.ArrowNamedDataSet | None = ...,
        fragment_id: builtins.str = ...,
    ) -> None: ...
    def HasField(self, field_name: typing.Literal["add_block", b"add_block", "add_rows", b"add_rows", "arrow_add_rows", b"arrow_add_rows", "new_element", b"new_element", "type", b"type"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing.Literal["add_block", b"add_block", "add_rows", b"add_rows", "arrow_add_rows", b"arrow_add_rows", "fragment_id", b"fragment_id", "new_element", b"new_element", "type", b"type"]) -> None: ...
    def WhichOneof(self, oneof_group: typing.Literal["type", b"type"]) -> typing.Literal["new_element", "add_block", "add_rows", "arrow_add_rows"] | None: ...

global___Delta = Delta
