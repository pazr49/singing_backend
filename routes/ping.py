from database.connection import establish_connection, execute_query
def ping():

    # results = execute_query(establish_connection(), 'SELECT *s FROM songs')
    return 'pong'