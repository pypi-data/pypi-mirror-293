# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Required, Annotated, TypedDict

from .._utils import PropertyInfo

__all__ = ["TopLevelImportRowsParams"]


class TopLevelImportRowsParams(TypedDict, total=False):
    database_id: Required[Annotated[str, PropertyInfo(alias="databaseId")]]

    creation_block_id: Annotated[str, PropertyInfo(alias="creationBlockId")]

    creation_parent_id: Annotated[str, PropertyInfo(alias="creationParentId")]
