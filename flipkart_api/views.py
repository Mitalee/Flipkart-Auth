from flask import render_template, redirect, session, url_for, Response, abort, request, current_app as app

from flask import Blueprint

import settings
import json

from .client import AuthClient

api = Blueprint('flipkart_api', __name__,
    template_folder='templates',
    static_folder='static'
)

@api.route('/', methods=('GET', 'POST'))
def index():
	#return('hi')
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
    #print('STATE IN CALLBACK IS ', session['state'])
    
    auth_client = AuthClient(
        app.config['APP_ID'], 
        app.config['APP_SECRET'], 
        app.config['REDIRECT_URI'], 
        app.config['ENVIRONMENT'],
        state_token=session.get('state', None),
    )
    print('AUTH CLIENT STATE TOKEN IN CALLBACK IS: ', auth_client.state_token)
    state_tok = request.args.get('state', None)
    error = request.args.get('error', None)

    print('STATE TOKEN AND ERROR ARE: ', state_tok, error)
    
    if error == 'access_denied':
        return redirect(url_for('/'))
    
    if state_tok is None:
        print('STATE TOKEN IS NONE')
        #return HttpResponseBadRequest()
        abort(400)
    elif state_tok != auth_client.state_token:  
        #return ('unauthorized', status=401)
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
        # just printing status_code here but it can be used for retry workflows, etc
        print(str(e))
    except Exception as e:
        print(e)
    return redirect(url_for('flipkart_api.connected'))

@api.route('/connected', methods=('GET', 'POST'))
def connected():
    auth_client = AuthClient(
        app.config['APP_ID'], 
        app.config['APP_SECRET'], 
        app.config['REDIRECT_URI'], 
        app.config['ENVIRONMENT'],
        access_token=session.get('access_token', None), 
        refresh_token=session.get('refresh_token', None), 
    )

    return render_template('connected.html')


@api.route('/mytokens', methods=('GET', 'POST'))
def tokens():
	data = {
	'access_token': session.get('access_token', None), 
	'refresh_token': session.get('refresh_token', None)
	}
	return Response(json.dumps(data), status=200, mimetype='application/json')