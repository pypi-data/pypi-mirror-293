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
import google.protobuf.internal.enum_type_wrapper
import google.protobuf.message
import streamlit.proto.AppPage_pb2
import sys
import typing

if sys.version_info >= (3, 10):
    import typing as typing_extensions
else:
    import typing_extensions

DESCRIPTOR: google.protobuf.descriptor.FileDescriptor

@typing.final
class Navigation(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    class _Position:
        ValueType = typing.NewType("ValueType", builtins.int)
        V: typing_extensions.TypeAlias = ValueType

    class _PositionEnumTypeWrapper(google.protobuf.internal.enum_type_wrapper._EnumTypeWrapper[Navigation._Position.ValueType], builtins.type):
        DESCRIPTOR: google.protobuf.descriptor.EnumDescriptor
        HIDDEN: Navigation._Position.ValueType  # 0
        """do not display the navigation"""
        SIDEBAR: Navigation._Position.ValueType  # 1
        """display navigation in the sidebar"""

    class Position(_Position, metaclass=_PositionEnumTypeWrapper):
        """Position of the Navigation"""

    HIDDEN: Navigation.Position.ValueType  # 0
    """do not display the navigation"""
    SIDEBAR: Navigation.Position.ValueType  # 1
    """display navigation in the sidebar"""

    SECTIONS_FIELD_NUMBER: builtins.int
    APP_PAGES_FIELD_NUMBER: builtins.int
    POSITION_FIELD_NUMBER: builtins.int
    PAGE_SCRIPT_HASH_FIELD_NUMBER: builtins.int
    position: global___Navigation.Position.ValueType
    page_script_hash: builtins.str
    """The script hash for the page identified by st.navigation"""
    @property
    def sections(self) -> google.protobuf.internal.containers.RepeatedScalarFieldContainer[builtins.str]: ...
    @property
    def app_pages(self) -> google.protobuf.internal.containers.RepeatedCompositeFieldContainer[streamlit.proto.AppPage_pb2.AppPage]: ...
    def __init__(
        self,
        *,
        sections: collections.abc.Iterable[builtins.str] | None = ...,
        app_pages: collections.abc.Iterable[streamlit.proto.AppPage_pb2.AppPage] | None = ...,
        position: global___Navigation.Position.ValueType = ...,
        page_script_hash: builtins.str = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing.Literal["app_pages", b"app_pages", "page_script_hash", b"page_script_hash", "position", b"position", "sections", b"sections"]) -> None: ...

global___Navigation = Navigation
