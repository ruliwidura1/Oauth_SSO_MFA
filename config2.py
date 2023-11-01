from flask import Flask, request, redirect, render_template
from flask_login import LoginManager, UserMixin, login_user, login_required, current_user, logout_user
import pyotp  # Pustaka untuk Google Authenticator

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Ganti dengan kunci rahasia Anda

login_manager = LoginManager()
login_manager.init_app(app)

# Daftar pengguna sederhana (biasanya digunakan dari database)
users = {
    'user1': {'password': 'password123', 'secret_key': 'your_secret_key'},
    'user2': {'password': 'securepass', 'secret_key': 'another_secret_key'}
}

class User(UserMixin):
    pass

@login_manager.user_loader
def user_loader(user_id):
    if user_id not in users:
        return

    user = User()
    user.id = user_id
    return user

@app.route('/')
def index():
    return 'Selamat datang! <a href="/login">Masuk</a>'

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in users and users[username]['password'] == password:
            user = User()
            user.id = username
            login_user(user)
            return redirect('/mfa')

    return render_template('login.html')

@app.route('/mfa', methods=['GET', 'POST'])
@login_required
def mfa():
    if request.method == 'POST':
        totp = pyotp.TOTP(users[current_user.id]['secret_key'])
        token = request.form['token']
        if totp.verify(token):
            return 'Otentikasi MFA berhasil!'
    return render_template('mfa.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return 'Anda telah keluar. <a href="/login">Masuk lagi</a>'

if __name__ == '__main__':
    app.run()
