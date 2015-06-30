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

@app.route('/login')
def login():
   # callback = url_for(
      #  'spotify_authorized',
      #  next=request.args.get('next') or request.referrer or None,
      #  _external=True
   # )
    print 'hello'
    return spotify.authorize(callback='/login/authorized')

@app.route('/login/authorized')
def spotify_authorized():
    print 'hello 2'
    resp = spotify.authorized_response()
    #if resp is None:
     #   flash(u'You denied the request to sign in.')
      #  return redirect(next_url)

    session['oauth_token'] = (resp['oauth_token'], '')
    session['spotify_user'] = resp['screen_name']

    print session['oauth_token']
    return render_template('thanks.html')

@app.route('/')
def thanks():
    return render_template('thanks.html')


@spotify.tokengetter
def get_spotify_token(token=None):
    return session.get('oauth_token')

if __name__ == '__main__':
    app.run()
