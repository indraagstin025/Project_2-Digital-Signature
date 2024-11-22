from flask import Flask, render_template, request, redirect, url_for, flash, session
from werkzeug.utils import secure_filename
import os
from controllers.auth_controller import login, register
from models.user import User
from models.document import Document
from middlewares import login_required

app = Flask(__name__)
app.secret_key = b'\x11\x91\xf9x\x870\xd2\x04\t\x8f\xe7\xa5\x98\xf7\xac\x94\x14\xf7*\xfb\x99#\xba\xea'  # Gantilah dengan kunci yang lebih aman

# Konfigurasi folder untuk menyimpan dokumen yang di-upload
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # Maksimum ukuran file 16MB
ALLOWED_EXTENSIONS = {'pdf', 'docx', 'txt'}

# Fungsi untuk memeriksa ekstensi file yang di-upload
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def home():
    """Halaman utama dengan pilihan login dan register"""
    return render_template('home.html')

@app.route('/dashboard', methods=['GET'])
@login_required
def dashboard():
    """Halaman dashboard yang menampilkan konten berbeda untuk admin dan user"""
    role = session.get('role')
    username = session.get('username')

    # Pastikan hanya user yang sudah login yang bisa mengakses dashboard
    if role == 'admin':
        return render_template('admin_dashboard.html', username=username)
    else:
        return render_template('user_dashboard.html', username=username)

@app.route('/login', methods=['GET', 'POST'])
def login_route():
    """Route untuk login"""
    if session.get('logged_in'):
        return redirect(url_for('dashboard'))  # Jika sudah login, redirect ke dashboard
    return login()  # Panggil fungsi login dari controller

@app.route('/register', methods=['GET', 'POST'])
def register_route():
    """Route untuk register"""
    return register()  # Panggil fungsi register dari controller

@app.route('/profile/<username>', methods=['GET'])
@login_required
def profile(username):
    """Profil pengguna setelah login"""
    user = User.get_user_by_username(username)
    if user:
        documents = Document.get_documents_by_user(user['id'])
        return render_template('profile.html', user=user, documents=documents)
    else:
        flash('User not found', 'danger')
        return redirect(url_for('login_route'))  # Redirect ke halaman login jika user tidak ditemukan

@app.route('/upload_document', methods=['POST'])
@login_required
def upload_document():
    """Route untuk upload dokumen"""
    if 'file' not in request.files:
        flash('No file part', 'danger')
        return redirect(request.url)

    file = request.files['file']
    if file.filename == '':
        flash('No selected file', 'danger')
        return redirect(request.url)

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)

        if not os.path.exists(app.config['UPLOAD_FOLDER']):
            os.makedirs(app.config['UPLOAD_FOLDER'])

        file.save(file_path)
        user_id = request.form['user_id']
        Document.create_document(user_id, filename, file_path)

        flash('Document uploaded successfully!', 'success')
        return redirect(url_for('profile', username=session.get('username')))
    else:
        flash('Invalid file format. Only PDF, DOCX, and TXT are allowed.', 'danger')
        return redirect(request.url)

@app.route('/logout')
def logout():
    """Route untuk logout pengguna"""
    session.clear()  # Menghapus seluruh sesi
    flash('You have been logged out.', 'info')  # Pesan logout
    return redirect(url_for('home'))  # Redirect ke halaman login

@app.after_request
def add_no_cache_headers(response):
    """Middleware untuk menambahkan header pencegahan cache pada halaman penting"""
    # Menambahkan header untuk mencegah cache setelah logout
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '-1'
    return response


if __name__ == '__main__':
    app.run(debug=True)
