"""Mixins for *arr API data models.
"""
from dataclasses import dataclass

from downloadcarr import enums


@dataclass(frozen=True)
class PageMixin:
    """Mixin implementing interface for paginated records.
    """

    page: int
    pageSize: int
    sortKey: enums.SortKey
    sortDirection: enums.SortDirection
    totalRecords: int
    records: NotImplemented  # Implement in subclasses
