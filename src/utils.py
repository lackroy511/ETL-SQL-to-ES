import logging

import requests

MOVIE_COLUMN_NAMES = {
    0: 'id',
    1: 'genre',
    2: 'director',
    3: 'writer',
    4: 'title',
    5: 'plot',
    7: 'imdb_rating',
    8: 'writers',
}


def movie_row_to_dict(row: tuple) -> dict:
    movie_data = {}
    for key, value in MOVIE_COLUMN_NAMES.items():
        movie_data.update(
            {value: row[key]},
        )

    return movie_data


def person_row_to_dict(person_rows: tuple, person_type: str) -> dict:
    person_names = ''
    person_data = {}
    person_data[person_type] = []
    for person in person_rows:
        if person[1]:
            person_names += person[1] + ', '
            person_data[person_type].append(
                {
                    'id': person[0],
                    'name': person[1],
                },
            )

    if person_names:
        person_data.update(
            {f'{person_type}_names': person_names.rstrip(', ')},
        )

    return person_data


def load_to_es(db_path: str, data: str) -> None:

    logger = logging.getLogger()

    request = requests.post(
        url='http://elastic:9200/movies/_bulk?filter_path=items.*.error',
        data=data,
        headers={'Content-Type': 'application/json'},
    )
    response = request.json()

    for item in response.get('items', []):
        error_message = item['index'].get('error')
        if error_message:
            logger.error(error_message)
