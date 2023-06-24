from flask import jsonify
from database.connection import execute_query, establish_connection

def get_song_by_id(song_id):
    # Create cursor to execute SQL queries
    db = establish_connection()
    print("printing song id")
    print(song_id)
    result = execute_query(db, "SELECT * FROM songs WHERE id = '" + str(song_id) + "'")[0]
    print(result)
    # Return result as JSON
    if result:
        song = {
            'id': result[0],
            'name': result[1],
            'num_parts': result[2],
            'backing_track': result[3],
            'key': result[4],
        }
        return jsonify(song)
    else:
        return jsonify({'error': 'Song not found'}), 404

def get_songs():
    # Create cursor to execute SQL queries
    db = establish_connection()

    result = execute_query(db, "SELECT * FROM songs")
    print(result)
    # Return result as JSON
    if result:
        songs = []
        for row in result:
            song = {
                'id': row[0],
                'name': row[2],
                'parts': row[1],
                'backing_track': row[3],
            }
            songs.append(song)
        return jsonify(songs)
    else:
        return jsonify({'error': 'Song not found'}), 404

def get_parts(song_id):
    # Create cursor to execute SQL queries
    db = establish_connection()
    print("printing song id" + str(song_id))
    result = execute_query(db, "SELECT * FROM song_parts WHERE song_id = '" + str(song_id) + "'")
    print(result)
    # Return result as JSON
    if result:
        parts = []
        for row in result:
            part = {
                'id': row[0],
                'part': row[1],
                'song_id': row[2],
                'music_url': row[3],
                'name': row[4],
            }
            parts.append(part)
        return jsonify(parts)
    else:
        return jsonify({'error': 'Song not found'}), 404