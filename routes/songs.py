from flask import jsonify
from database.connection import execute_query, establish_connection

def get_song(song_id):
    # Create cursor to execute SQL queries
    db = establish_connection()
    print("printing song id")
    print(song_id)
    result = execute_query(db, "SELECT * FROM songs WHERE id = " + str(song_id))[0]
    print(result)
    # Return result as JSON
    if result:
        song = {
            'id': result[0],
            'name': result[1],
            'num_parts': result[2]
        }
        return jsonify(song)
    else:
        return jsonify({'error': 'Song not found'}), 404


def get_parts(song_id):
    # Create cursor to execute SQL queries
    db = establish_connection()

    result = execute_query(db, "SELECT * FROM song_parts WHERE song_id = " + str(song_id))
    print(result)
    # Return result as JSON
    if result:
        parts = []
        for row in result:
            part = {
                'id': row[0],
                'part': row[1],
                'song_id': row[2],
                'music_url': row[3]
            }
            parts.append(part)
        return jsonify(parts)
    else:
        return jsonify({'error': 'Song not found'}), 404