from flask import Flask, jsonify, request, abort
import requests
from flask_cors import CORS

app = Flask('movies_service')
CORS(app)

ES_BASE_URL = 'http://elastic:9200'


@app.route('/api/movies', methods=['GET'], strict_slashes=False)
def movies_list() -> str:

    page = request.args.get('page', default=1, type=int)
    limit = request.args.get('limit', default=50, type=int)
    sort_field = request.args.get('sort_by', default='id', type=str)
    sort_order = request.args.get('sort_order', default='asc', type=str)
    search = request.args.get('search', default='', type=str)

    query = {
        'from': ((page if page > 0 else 1) - 1) * limit,
        'size': limit,
        'sort':  [
            {
                sort_field: {
                    'order': sort_order,
                },
            },
        ],
    }
    if search:
        query['query'] = {
            'multi_match': {
                'query': search,
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

    response = requests.get(
        url=f'{ES_BASE_URL}/movies/_search',
        headers={'Content-Type': 'application/json'},
        json=query,
    )
    
    result = []
    hits = response.json()['hits']['hits']
    for hit in hits:
        result.append({
            'id': hit['_id'],
            'title': hit['_source']['title'],
            'imdb_rating': hit['_source']['imdb_rating'],
            
        })

    return jsonify(result)


@app.route('/api/movies/<movie_id>', methods=['GET'])
def movie_details(movie_id: str) -> str:
    # Код, получающий данные из ES об одном фильме
    url = f'{ES_BASE_URL}/movies/_doc/{movie_id}'
    
    response = requests.get(
        url=url,
        headers={'Content-Type': 'application/json'},
    )
    
    if response.status_code == 404:
        response = jsonify('Фильм не найден')
        response.status_code = 404
        return response
    
    result = {}
    result['id'] = response.json()['_id']
    result = response.json()['_source']

    return jsonify(result)


if __name__ == '__main__':
    app.run()
