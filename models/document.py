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

class Document:
    @staticmethod
    def create_document(user_id, document_name, document_path):
        """Membuat dokumen baru di database"""
        # Validasi input
        if not isinstance(user_id, int):
            raise ValueError("user_id harus berupa integer")
        if not document_name:
            raise ValueError("Nama dokumen tidak boleh kosong")
        if not document_path:
            raise ValueError("Path dokumen tidak boleh kosong")
        
        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                'INSERT INTO documents (user_id, document_name, document_path, signed) VALUES (%s, %s, %s, %s)',
                (user_id, document_name, document_path, False)
            )
            conn.commit()
        except mysql.connector.Error as e:
            conn.rollback()
            raise e
        finally:
            conn.close()

