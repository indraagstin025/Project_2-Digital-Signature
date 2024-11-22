import mysql.connector

# Fungsi untuk membuat koneksi ke database MySQL
def get_db_connection():
    conn = mysql.connector.connect(
        host='localhost',
        user='root',  # Ganti dengan username MySQL Anda
        password='',  # Ganti dengan password MySQL Anda
        database='flask_crud_db'  # Ganti dengan nama database Anda
    )
    return conn

# Model Document
class Document:
    """Model untuk mengelola dokumen yang di-upload oleh pengguna"""

    @staticmethod
    def get_documents_by_user(user_id):
        """Mendapatkan semua dokumen yang di-upload oleh pengguna"""
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute('SELECT * FROM documents WHERE user_id = %s', (user_id,))
        documents = cursor.fetchall()
        conn.close()
        return documents

    @staticmethod
    def create_document(user_id, document_name, document_path):
        """Membuat dokumen baru di database"""
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO documents (user_id, document_name, document_path, signed) VALUES (%s, %s, %s, %s)',
            (user_id, document_name, document_path, False)  # status signed default False
        )
        conn.commit()
        conn.close()
