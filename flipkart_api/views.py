from flask import (
	Blueprint,
	render_template,
	redirect,
	session,
	url_for,
	Response,
	abort,
	request,
	current_app as app
	)

import json

from .client import AuthClient

api = Blueprint('flipkart_api', __name__,
    template_folder='templates'
)

@api.route('/api_data_call/', methods=('GET', 'POST'))
def flipkart_request():
    auth_client = AuthClient(
        app.config['APP_ID'],
        app.config['APP_SECRET'],
        app.config['REDIRECT_URI'],
        app.config['ENVIRONMENT'],
        access_token=session.get('access_token', None),
        refresh_token=session.get('refresh_token', None),
    )


    data = auth_client.get_data()
    response = json.loads(data.content)
    print("RESPONSE IS: ", response)

    return Response(json.dumps(response), status=200, mimetype='application/json')



@api.route('/', methods=('GET', 'POST'))
def index():
	return render_template('index.html')

@api.route('/oauth/', methods=('GET', 'POST'))
def oauth():
    auth_client = AuthClient(
        app.config['APP_ID'],
        app.config['APP_SECRET'],
        app.config['REDIRECT_URI'],
        app.config['ENVIRONMENT']
    )

    print(str(auth_client))
    url = auth_client.get_authorization_url()
    print('AUTH URL IS: ', url)
    session['state'] = auth_client.state_token

    print('STATE IN OAUTH IS ', session['state'])
    try: 
    	return redirect(url)
    except Exception as e:
    	print(str(e))

@api.route('/callback', methods=('GET', 'POST'))
def callback():
    
    auth_client = AuthClient(
        app.config['APP_ID'], 
        app.config['APP_SECRET'], 
        app.config['REDIRECT_URI'], 
        app.config['ENVIRONMENT'],
        state_token=session.get('state', None),
    )

    state_tok = request.args.get('state', None)
    error = request.args.get('error', None)


    
    if error == 'access_denied':
        return redirect(url_for('/'))
    
    if state_tok is None:
        print('STATE TOKEN IS NONE')
        abort(400)
    elif state_tok != auth_client.state_token:  
        abort(401)
    
    auth_code = request.args.get('code', None)


    if auth_code is None:
        print('AUTH CODE IS NONE')
        return abort(400)

    try:
        auth_client.get_access_token(auth_code)
        session['access_token'] = auth_client.access_token
        session['refresh_token'] = auth_client.refresh_token
        print('ACCESS TOKEN IS: ', session['access_token'])
        print('REFRESH TOKEN IS: ', session['refresh_token'])
    except Exception as e:

        print(str(e))
    except Exception as e:
        print(e)
    return redirect(url_for('flipkart_api.connected'))

@api.route('/connected', methods=('GET', 'POST'))
def connected():
    return render_template('connected.html')


@api.route('/mytokens', methods=('GET', 'POST'))
def tokens():
	data = {
	'access_token': session.get('access_token', None), 
	'refresh_token': session.get('refresh_token', None)
	}
	return Response(json.dumps(data), status=200, mimetype='application/json')