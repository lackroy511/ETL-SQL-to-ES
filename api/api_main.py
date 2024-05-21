from flask import Flask, jsonify, request


app = Flask('movies_service')


@app.route('/api/movies', methods=['GET'], strict_slashes=False)
def movies_list() -> str:
    # Код, получающий данные из ES об отфильтрованном по request.args
    # списке фильмов
    
    filters = request.args.to_dict()
    
    result = {
        'some_key': 'some_value',
    }
    return jsonify(result)


@app.route('/api/movies/<movie_id>', methods=['GET'])
def movie_details(movie_id: str) -> str:
    # Код, получающий данные из ES об одном фильме

    result = {
        'some_key': 'some_value',
    }

    return jsonify(result)


if __name__ == '__main__':
    app.run(port=8000)
