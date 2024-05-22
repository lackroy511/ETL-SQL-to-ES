import requests
from flask import Flask, Request, jsonify, request
from flask_cors import CORS
from pydantic import ValidationError

from api.utils.movies_list import form_query, form_response

app = Flask('movies_service')
CORS(app)

ES_BASE_URL = 'http://elastic:9200'


@app.route('/api/movies', methods=['GET'], strict_slashes=False)
def movies_list() -> str:

    try:
        query = form_query(request)
    except ValidationError as e:
        response = jsonify(e.errors(include_url=False))
        response.status_code = 422
        return response

    response = requests.get(
        url=f'{ES_BASE_URL}/movies/_search',
        headers={'Content-Type': 'application/json'},
        json=query,
    )
    
    result = form_response(response_json=response.json())

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
    app.run(port=8000)
