from flask import Flask, redirect, url_for, session, request, render_template
from flask_oauthlib.client import OAuth

app = Flask(__name__)
app.debug = True
app.secret_key = 'development'

oauth = OAuth()
spotify = oauth.remote_app(
    'spotify',
    consumer_key='66dfb3e0319e450d8de499b92ee09eb8',
    consumer_secret='0837db16615146149427e3225781f4de',
    request_token_params={'scope':'playlist-modify-public'},
    base_url='https://accounts.spotify.com',
    request_token_url=None,
    access_token_url='/api/token',
    authorize_url='https://accounts.spotify.com/authorize')

@app.route('/')
def index():
    print 'homepage'
    return redirect(url_for('login'))

@app.route('/login')
def login():
    print 'redirect to login'
    return spotify.authorize(callback='/login/authorized')

@app.route('/login/authorized')
def spotify_authorized():
    print 'reached authorized'
    resp = spotify.authorized_response()
    if resp is None:
        return 'Access denied: reason={0} error={1}'.format(
            request.args['error_reason'],
            request.args['error_description'])

    if isinstance(resp, OAuthException):
        return 'Access denied: {0}'.format(resp.message)

    session['oauth_token'] = (resp['access_token'], '')
    return render_template('thanks.html')

@spotify.tokengetter
def get_spotify_token(token=None):
    return session.get('oauth_token')

if __name__ == '__main__':
    app.run()
