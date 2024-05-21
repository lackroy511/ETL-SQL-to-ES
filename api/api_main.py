from flask import Flask, jsonify, request
import requests

app = Flask('movies_service')

ES_BASE_URL = 'http://elastic:9200'


@app.route('/api/movies', methods=['GET'], strict_slashes=False)
def movies_list() -> str:
    url = f'{ES_BASE_URL}/movies/_search'
    
    query = {
        'from': 0,
        'size': 10,
        'sort': [
        ],
        'query': {
            'multi_match': {
                'query': '',
                'fuzziness': 'auto',
                'fields': [
                    'title^5',
                    'description^4',
                    'genre^3',
                    'actors_names^3',
                    'writers_names^2',
                ],
            },
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
