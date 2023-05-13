import mysql.connector

def establish_connection():
    cnx = mysql.connector.connect(
        host='localhost',
        user='root',
        password='robert123',
        database='singing_app'
    )
    return cnx

def execute_query(connection, query):
    cursor = connection.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    cursor.close()
    return results
