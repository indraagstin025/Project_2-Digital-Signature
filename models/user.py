import mysql.connector

# Fungsi untuk membuat koneksi ke database MySQL
def get_db_connection():
    conn = mysql.connector.connect(
        host='localhost',
        user='root',  # ganti dengan username MySQL Anda
        password='',  # ganti dengan password MySQL Anda
        database='flask_crud_db'  # ganti dengan nama database Anda
    )
    return conn

# Model User
class User:
    """Model untuk mengelola data pengguna (login dan register)"""
    
    @staticmethod
    def get_user_by_username(username):
        """Mendapatkan data pengguna berdasarkan username"""
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute('SELECT * FROM users WHERE username = %s', (username,))
        user = cursor.fetchone()
        conn.close()
        return user
    
    @staticmethod
    def create_user(username, password, email, role):
        """Membuat pengguna baru di database"""
        conn = get_db_connection()
        cursor = conn.cursor()
        # Periksa jika pengguna dengan username yang sama sudah ada
        cursor.execute('SELECT * FROM users WHERE username = %s', (username,))
        existing_user = cursor.fetchone()
        if existing_user:
            conn.close()
            raise Exception("Username already exists!")
        
        # Password di sini sudah dalam bentuk hash
        cursor.execute('INSERT INTO users (username, password, email, role) VALUES (%s, %s, %s, %s)', 
                       (username, password, email, role))
        conn.commit()
        conn.close()


# Model Document
class Document:
    """Model untuk mengelola data dokumen yang di-upload oleh pengguna"""
    
    @staticmethod
    def create_document(user_id, document_name, document_path):
        """Membuat dokumen baru di database"""
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO documents (user_id, document_name, document_path) VALUES (%s, %s, %s)', 
                       (user_id, document_name, document_path))
        conn.commit()
        conn.close()
    
    @staticmethod
    def get_documents_by_user(user_id):
        """Mendapatkan semua dokumen yang dimiliki oleh pengguna tertentu"""
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute('SELECT * FROM documents WHERE user_id = %s', (user_id,))
        documents = cursor.fetchall()
        conn.close()
        return documents
