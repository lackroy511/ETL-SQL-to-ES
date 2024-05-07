import sqlite3
import json


class SQLiteConnector:
    def __init__(self, db_path: str) -> None:
        self.db_path = db_path
        self.connection = None
        self.cursor = None

    def __enter__(self):
        self.connection = sqlite3.connect(self.db_path)
        self.cursor = self.connection.cursor()
        return self
    
    def __exit__(self, exc_type, exc_value, traceback):
        self.connection.commit()
        self.cursor.close()
        self.connection.close()


class MoviesDB(SQLiteConnector):
    def get_movies(self):
        self.cursor.execute('SELECT * FROM movies')
        return self.cursor.fetchall()

    def get_actors_by_movie_id(self, movie_id):
        query = 'SELECT actor_id, name FROM movie_actors ' + \
                'JOIN actors ON movie_actors.actor_id = actors.id ' + \
                f"WHERE movie_id = '{movie_id}';"
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def get_writers(self, writer_id: str, writer_ids: dict):
        if writer_id:
            query = f"SELECT * FROM writers WHERE id = '{writer_id}';"
            self.cursor.execute(query)
        
        if writer_ids:
            writer_ids = json.loads(writer_ids)
            query = 'SELECT * FROM writers WHERE id IN ' + \
                    f"{tuple([writer['id'] for writer in writer_ids])};"
            self.cursor.execute(query)

        return self.cursor.fetchall()
