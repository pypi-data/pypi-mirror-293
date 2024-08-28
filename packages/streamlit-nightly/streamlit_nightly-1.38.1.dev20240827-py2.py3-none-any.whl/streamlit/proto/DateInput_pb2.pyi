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
import collections.abc
import google.protobuf.descriptor
import google.protobuf.internal.containers
import google.protobuf.message
import streamlit.proto.LabelVisibilityMessage_pb2
import typing

DESCRIPTOR: google.protobuf.descriptor.FileDescriptor

@typing.final
class DateInput(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    ID_FIELD_NUMBER: builtins.int
    LABEL_FIELD_NUMBER: builtins.int
    DEFAULT_FIELD_NUMBER: builtins.int
    MIN_FIELD_NUMBER: builtins.int
    MAX_FIELD_NUMBER: builtins.int
    IS_RANGE_FIELD_NUMBER: builtins.int
    HELP_FIELD_NUMBER: builtins.int
    FORM_ID_FIELD_NUMBER: builtins.int
    VALUE_FIELD_NUMBER: builtins.int
    SET_VALUE_FIELD_NUMBER: builtins.int
    DISABLED_FIELD_NUMBER: builtins.int
    LABEL_VISIBILITY_FIELD_NUMBER: builtins.int
    FORMAT_FIELD_NUMBER: builtins.int
    id: builtins.str
    label: builtins.str
    min: builtins.str
    max: builtins.str
    is_range: builtins.bool
    help: builtins.str
    form_id: builtins.str
    set_value: builtins.bool
    disabled: builtins.bool
    format: builtins.str
    @property
    def default(self) -> google.protobuf.internal.containers.RepeatedScalarFieldContainer[builtins.str]: ...
    @property
    def value(self) -> google.protobuf.internal.containers.RepeatedScalarFieldContainer[builtins.str]: ...
    @property
    def label_visibility(self) -> streamlit.proto.LabelVisibilityMessage_pb2.LabelVisibilityMessage: ...
    def __init__(
        self,
        *,
        id: builtins.str = ...,
        label: builtins.str = ...,
        default: collections.abc.Iterable[builtins.str] | None = ...,
        min: builtins.str = ...,
        max: builtins.str = ...,
        is_range: builtins.bool = ...,
        help: builtins.str = ...,
        form_id: builtins.str = ...,
        value: collections.abc.Iterable[builtins.str] | None = ...,
        set_value: builtins.bool = ...,
        disabled: builtins.bool = ...,
        label_visibility: streamlit.proto.LabelVisibilityMessage_pb2.LabelVisibilityMessage | None = ...,
        format: builtins.str = ...,
    ) -> None: ...
    def HasField(self, field_name: typing.Literal["label_visibility", b"label_visibility"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing.Literal["default", b"default", "disabled", b"disabled", "form_id", b"form_id", "format", b"format", "help", b"help", "id", b"id", "is_range", b"is_range", "label", b"label", "label_visibility", b"label_visibility", "max", b"max", "min", b"min", "set_value", b"set_value", "value", b"value"]) -> None: ...

global___DateInput = DateInput
