from flask import render_template, request, redirect, url_for, flash, session, jsonify
from models.user import User
from models.document import Document
from werkzeug.security import generate_password_hash, check_password_hash  
from flask import session


def login():
    """Controller untuk proses login pengguna"""
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if not username or not password:
            flash('Username and password are required!', 'danger')
            return redirect(url_for('login_route'))

        user = User.get_user_by_username(username)

        if not user:
            flash('Invalid username or password!', 'danger')
            return redirect(url_for('login_route'))

        if not check_password_hash(user['password'], password):
            flash('Invalid username or password!', 'danger')
            return redirect(url_for('login_route'))

        # Simpan session untuk login
        session['logged_in'] = True
        session['username'] = user['username']
        session['role'] = user['role']

        flash(f'Welcome, {user["username"]}!', 'success')

        return redirect(url_for('dashboard'))  # Pastikan hanya ada satu pengalihan ke dashboard setelah login sukses

    return render_template('login.html')


def register():
    """Controller untuk proses registrasi pengguna"""
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        email = request.form.get('email')  
        role = request.form.get('role', 'user') 

       
        print(f"Username: {username}, Password: {password}, Confirm Password: {confirm_password}, Email: {email}, Role: {role}")

   
        if not username or not password or not confirm_password or not email:
            flash('All fields are required!', 'danger')
            return redirect(url_for('register_route'))

        if password != confirm_password:
            flash('Passwords do not match!', 'danger')
            return redirect(url_for('register_route'))
    
        if User.get_user_by_username(username):
            flash('Username already exists!', 'danger')
            return redirect(url_for('register_route'))

        try:
            hashed_password = generate_password_hash(password)
            User.create_user(username=username, password=hashed_password, email=email, role=role)
            flash('Registration successful! Please log in.', 'success')
            return redirect(url_for('login_route'))
        
        except Exception as e:
            flash(f'Error during registration: {e}', 'danger')
            return redirect(url_for('register_route'))
    
    return render_template('register.html')

class DocumentController:
    @staticmethod
    def upload_document():
        """Handle upload document request"""
        user_id = request.form.get('user_id')
        document_name = request.form.get('document_name')
        file = request.files.get('document')

        # Validasi user_id
        if not user_id or not user_id.strip().isdigit():
            return jsonify({'error': 'user_id tidak valid atau hilang'}), 400
        user_id = int(user_id)

        # Validasi input
        if not document_name or not file:
            return jsonify({'error': 'Nama Dokumen dan file dokumen diperlukan'}), 400

        # Simpan file dan ambil path
        document_path = DocumentController.save_uploaded_file(file)

        # Simpan ke database
        try:
            Document.create_document(user_id, document_name, document_path)
            return jsonify({"message": "Document uploaded successfully"}), 200
        except Exception as e:
            print(f"Error while creating document: {e}")
            return jsonify({"error": str(e)}), 500

    @staticmethod
    def save_uploaded_file(file):
        """Menyimpan file yang di-upload ke direktori tertentu"""
        import os

        upload_path = "uploads/"
        if not os.path.exists(upload_path):
            os.makedirs(upload_path)

        file_path = os.path.join(upload_path, file.filename)
        file.save(file_path)
        return file_path

    
    


