# Oauth_SSO_MFA
Mengenal dan memepelajari Oauth SSO dan MFA
from flask import Flask, request, redirect, session, url_for
from flask_oauthlib.client import OAuth

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Ganti dengan kunci rahasia Anda

oauth = OAuth(app)

# Konfigurasi OAuth dengan informasi dari penyedia OAuth
oauth.remote_app(
    'example',
    consumer_key='your_consumer_key',        # Ganti dengan kunci OAuth Anda
    consumer_secret='your_consumer_secret',  # Ganti dengan rahasia OAuth Anda
    request_token_params=None,
    base_url='https://api.example.com/',
    request_token_url=None,
    access_token_method='POST',
    access_token_url='https://api.example.com/oauth/access_token',
    authorize_url='https://api.example.com/oauth/authorize'
)

@app.route('/')
def index():
    return 'Selamat datang! <a href="/login">Masuk dengan OAuth</a>'

@app.route('/login')
def login():
    return oauth.example.authorize(callback=url_for('authorized', _external=True))

@app.route('/logout')
def logout():
    session.pop('example_oauth', None)
    return redirect(url_for('index'))

@app.route('/login/authorized')
def authorized():
    response = oauth.example.authorized_response()
    if response is None or response.get('access_token') is None:
        return 'Akses ditolak: alasan = {} dan informasi = {}'.format(
            request.args['error'],
            request.args['error_description']
        )

    session['example_oauth'] = response
    user_info = oauth.example.get('user_info')
    return 'Selamat datang, {}'.format(user_info.data['username'])

@oauth.example.tokengetter
def get_example_oauth_token():
    return session.get('example_oauth')

if __name__ == '__main__':
    app.run()
