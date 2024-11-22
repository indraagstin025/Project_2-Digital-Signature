from flask import render_template, request, redirect, url_for, flash, session
from models.user import User
from werkzeug.security import generate_password_hash, check_password_hash  
from flask import session

def login():
    """Controller untuk proses login pengguna"""
    if request.method == 'POST':
        # Ambil data dari form login
        username = request.form.get('username')
        password = request.form.get('password')

        # Validasi input
        if not username or not password:
            flash('Username and password are required!', 'danger')
            return redirect(url_for('login_route'))

        # Cek apakah username ada di database
        user = User.get_user_by_username(username)
        if not user:
            flash('Invalid username or password!', 'danger')
            return redirect(url_for('login_route'))

        # Cek apakah password cocok
        if not check_password_hash(user['password'], password):
            flash('Invalid username or password!', 'danger')
            return redirect(url_for('login_route'))

        # Jika login berhasil, set session
        session['logged_in'] = True
        session['username'] = user['username']
        session['role'] = user['role']
        flash(f'Welcome, {user["username"]}!', 'success')
        return redirect(url_for('dashboard'))

    return render_template('login.html')

def register():
    """Controller untuk proses registrasi pengguna"""
    if request.method == 'POST':
        # Mengambil data dari form
        username = request.form.get('username')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        email = request.form.get('email')  # Pastikan email juga ada
        role = request.form.get('role', 'user')  # Default role 'user' jika tidak ada

        # Debugging: cek data yang dikirim
        print(f"Username: {username}, Password: {password}, Confirm Password: {confirm_password}, Email: {email}, Role: {role}")

        # Validasi input
        if not username or not password or not confirm_password or not email:
            flash('All fields are required!', 'danger')
            return redirect(url_for('register_route'))

        if password != confirm_password:
            flash('Passwords do not match!', 'danger')
            return redirect(url_for('register_route'))
        
        # Cek apakah username sudah ada
        if User.get_user_by_username(username):
            flash('Username already exists!', 'danger')
            return redirect(url_for('register_route'))

        try:
            # Enkripsi password
            hashed_password = generate_password_hash(password)
            # Buat user baru
            User.create_user(username=username, password=hashed_password, email=email, role=role)
            flash('Registration successful! Please log in.', 'success')
            return redirect(url_for('login_route'))
        except Exception as e:
            # Tangani error jika terjadi saat pembuatan pengguna
            flash(f'Error during registration: {e}', 'danger')
            return redirect(url_for('register_route'))
    
    return render_template('register.html')


