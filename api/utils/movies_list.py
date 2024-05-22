from flask import Request
from pydantic import ValidationError

from api.models import MoviesListParams


def form_query(request: Request) -> dict:
    
    params = MoviesListParams(**request.args.to_dict())

    query = {
        'from': (params.page - 1) * params.limit,
        'size': params.limit,
        'sort':  [
            {
                params.sort: {
                    'order': params.sort_order,
                },
            },
        ],
    }
    if params.search:
        query['query'] = {
            'multi_match': {
                'query': params.search,
                'fuzziness': 'auto',
                'fields': [
                    'title^1',
                    'description^2',
                    'genre^3',
                    'actors_names^4',
                    'writers_names^5',
                ],
            },
        }
    
    return query


def form_response(response_json: dict) -> list:
    result = []
    hits = response_json['hits']['hits']
    for hit in hits:
        result.append({
            'id': hit['_id'],
            'title': hit['_source']['title'],
            'imdb_rating': hit['_source']['imdb_rating'],
            
        })
    
    return result
