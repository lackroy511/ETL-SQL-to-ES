from enum import Enum
from pydantic import BaseModel
from typing import Literal


class SortOrder(str, Enum):
    asc = 'asc'
    desc = 'desc'


class SortField(str, Enum):
    id = 'id'
    film_title = 'title'
    imdb_rating = 'imdb_rating'


class MoviesListParams(BaseModel):
    page: int = 1
    limit: int = 50
    sort_field: Literal[
        SortField.id,
        SortField.film_title,
        SortField.imdb_rating,
    ] = 'id'
    sort_order: Literal[SortOrder.asc, SortOrder.desc] = SortOrder.asc
    search: str = None
