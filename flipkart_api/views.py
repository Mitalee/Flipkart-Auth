from flask import render_template, redirect, session, url_for, Response, abort

from flask import Blueprint

import settings

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
        settings.APP_ID, 
        settings.APP_SECRET, 
        settings.REDIRECT_URI, 
        settings.ENVIRONMENT
    )

    print(str(auth_client))
    url = auth_client.get_authorization_url()
    print('AUTH URL IS: ', url)
    session['state'] = auth_client.state_token
    try: 
    	return redirect(url)
    except Exception as e:
    	print(str(e))

@api.route('/callback', methods=('GET', 'POST'))
def callback(request):
    auth_client = AuthClient(
        settings.APP_ID, 
        settings.APP_SECRET, 
        settings.REDIRECT_URI, 
        settings.ENVIRONMENT, 
        state_token=request.session.get('state', None),
    )

    state_tok = request.GET.get('state', None)
    error = request.GET.get('error', None)

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
    
    auth_code = request.GET.get('code', None)


    if auth_code is None:
    	print('AUTH CODE IS NONE')
        return abort(400)

    try:
        auth_client.get_access_token(auth_code)
        session['access_token'] = auth_client.access_token
        session['refresh_token'] = auth_client.refresh_token
    except Exception as e:
        # just printing status_code here but it can be used for retry workflows, etc
        print(str(e))
    except Exception as e:
        print(e)
    return redirect(url_for('connected'))


def connected(request):
    auth_client = AuthClient(
        settings.APP_ID, 
        settings.APP_SECRET, 
        settings.REDIRECT_URI, 
        settings.ENVIRONMENT, 
        access_token=request.session.get('access_token', None), 
        refresh_token=request.session.get('refresh_token', None), 
        id_token=request.session.get('id_token', None),
    )

    return render_template('connected.html')