from flask import Flask, request, jsonify
import pymysql
from connection import config
import logging

app = Flask(__name__)
logging.basicConfig(filename='access.log', level=logging.INFO,
                    format='%(asctime)s [%(levelname)s] %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
access_logger = logging.getLogger('access_logger')

@app.before_request
def log_request_info():
    log_data = f"{request.remote_addr} - {request.method} {request.path} - {request.user_agent}"
    access_logger.info(log_data)

def get_db_connection():
    return pymysql.connect(**config)

def create_table():
    connection = get_db_connection()
    with connection.cursor() as cursor:
        create_table_query = """
        CREATE TABLE IF NOT EXISTS mybook (
            id INT AUTO_INCREMENT PRIMARY KEY,
            author VARCHAR(255),
            title VARCHAR(255),
            isbn BIGINT
        )
        """
        cursor.execute(create_table_query)
    connection.commit()
    connection.close()

create_table()

@app.route('/books', methods=['GET'])
def get_books():
    connection = get_db_connection()
    with connection.cursor() as cursor:
        select_query = "SELECT * FROM mybook"
        cursor.execute(select_query)
        books = cursor.fetchall()

    books_list = [
        {'id': book[0], 'author': book[1], 'title': book[2], 'isbn': book[3]}
        for book in books
    ]
    connection.close()
    return jsonify(books_list)

@app.route('/books', methods=['POST'])
def add_book():
    book_data = request.get_json()
    author = book_data.get('author')
    title = book_data.get('title')
    isbn = book_data.get('isbn')

    connection = get_db_connection()
    with connection.cursor() as cursor:
        insert_query = "INSERT INTO mybook (author, title, isbn) VALUES (%s, %s, %s)"
        cursor.execute(insert_query, (author, title, isbn))
    connection.commit()
    connection.close()

    return jsonify({'message': 'Book added successfully'}), 201

@app.route('/books/<int:book_id>', methods=['PUT'])
def update_book(book_id):
    book_data = request.get_json()
    author = book_data.get('author')
    title = book_data.get('title')
    isbn = book_data.get('isbn')

    connection = get_db_connection()
    with connection.cursor() as cursor:
        update_query = "UPDATE mybook SET author=%s, title=%s, isbn=%s WHERE id=%s"
        cursor.execute(update_query, (author, title, isbn, book_id))
    connection.commit()
    connection.close()

    return jsonify({'message': 'Book updated successfully'})

@app.route('/books/<int:book_id>', methods=['DELETE'])
def delete_book(book_id):
    connection = get_db_connection()
    with connection.cursor() as cursor:
        delete_query = "DELETE FROM mybook WHERE id=%s"
        cursor.execute(delete_query, (book_id,))
    connection.commit()
    connection.close()

    return jsonify({'message': 'Book deleted successfully'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
