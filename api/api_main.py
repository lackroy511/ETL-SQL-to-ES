from flask import Flask, jsonify, request
import requests

app = Flask('movies_service')

ES_BASE_URL = 'http://elastic:9200'


@app.route('/api/movies', methods=['GET'], strict_slashes=False)
def movies_list() -> str:
    url = f'{ES_BASE_URL}/movies/_search'

    page = request.args.get('page', default=1, type=int)
    limit = request.args.get('limit', default=50, type=int)
    sort_by = request.args.get('sort_by', default='id', type=str)
    sort_order = request.args.get('sort_order', default='asc', type=str)
    search = request.args.get('search', default='', type=str)

    query = {
        'from': (page - 1) * limit,
        'size': limit,
        'sort':  [
            {
                sort_by: {
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
                    'title^5',
                    'description^4',
                    'genre^3',
                    'actors_names^3',
                    'writers_names^2',
                ],
            },
        }

    response = requests.get(url)

    return response.json()


@app.route('/api/movies/<movie_id>', methods=['GET'])
def movie_details(movie_id: str) -> str:
    # Код, получающий данные из ES об одном фильме

    result = {
        'some_key': 'some_value',
    }

    return jsonify(result)


if __name__ == '__main__':
    app.run(port=8000)
