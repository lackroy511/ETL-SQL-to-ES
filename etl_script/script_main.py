import json

from etl_script.db_connector import MoviesDB
from etl_script.utils import (get_imdb_rating, load_to_es, movie_row_to_dict,
                              person_row_to_dict)


def main():
    result = ''
    with MoviesDB('db.sqlite') as db:
        movies = db.get_movies()
        for movie in movies:
            movie = movie_row_to_dict(movie)

            actors = db.get_actors_by_movie_id(movie['id'])
            actors = person_row_to_dict(actors, 'actors')

            writers = db.get_writers(movie['writer'], movie['writers'])
            writers = person_row_to_dict(writers, 'writers')

            es_movie_meta_data = {
                'index': {'_index': 'movies', '_id': movie['id']},
            }
            es_movie_data = {
                'id': movie.get('id'),
                'imdb_rating': get_imdb_rating(movie.get('imdb_rating')),
                'genres': movie.get('genre'),
                'title': movie.get('title'),
                'description': movie.get('plot'),
                'directors_names': movie.get('director'),
                'actors_names': actors.get('actors_names'),
                'writers_names': writers.get('writers_names'),
                'actors': actors.get('actors'),
                'writers': writers.get('writers'),
            }
            result += json.dumps(es_movie_meta_data, ensure_ascii=False) + '\n'
            result += json.dumps(es_movie_data, ensure_ascii=False) + '\n'

    load_to_es(
        db_path='http://elastic:9200/movies/_bulk?filter_path=items.*.error',
        data=result,
    )


if __name__ == '__main__':
    main()
