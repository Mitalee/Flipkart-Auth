from flask import Flask, session
from flipkart_api.views import api
import settings

app = Flask(__name__)
#app.secret_key = "super secret key"

app.config.from_object('settings')

#app.config.from_pyfile('settings.cfg')

# app.config['SESSION_TYPE'] = 'filesystem'
# app.config['SECRET_KEY'] = 'hitherehellothere'
#sess.init_app(app)

app.secret_key = app.config['SECRET_KEY']
app.register_blueprint(api)

app.run(host='0.0.0.0',port='8001', debug=True)

#curl -X POST https://api.flipkart.net/oauth-service/oauth/token?grant_type=authorization_code&code=1noEeP&client_id=11a408bb3b648b6a2a62191028a2858a18997&client_secret=734c4c025c6b163dd5ae7c021c9459d6&redirect_uri=https%3A%2F%2Foauthdebugger.com%2Fdebug