from gevent import monkey
#need to allow unpatching
monkey.patch_all()
import gevent
from geventwebsocket.handler import WebSocketHandler
from gevent.pywsgi import WSGIServer
from flask import Flask, request, g, session, redirect, url_for, jsonify, current_app
import json, gevent, requests
from werkzeug.exceptions import HTTPException
from functools import wraps
from werkzeug.security import gen_salt

from airypi import utils
from airypi.callback_dict import CallbackDict
import device
from flask_socketio import SocketIO, disconnect
from airypi import message_queue
import datetime

from flask_oauthlib.client import OAuth
from airypi import remote_obj

import traceback

import os

app = Flask(__name__)
app.config['PERMANENT_SESSION_LIFETIME'] = datetime.timedelta(365*10)
oauth = OAuth(app)
socketio = SocketIO(app)

server_url = 'https://www.airypi.com'

oauth_server = oauth.remote_app('app_server',
    base_url=server_url,
    access_token_url=server_url + '/oauth/token',
    authorize_url=server_url + '/oauth/authorize',
    request_token_params={'scope': 'id'},
    consumer_key = "placeholder",
    consumer_secret = "placeholder"
)

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if utils.get_hidden_session('user_id') is None:
            return redirect(url_for('login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function

def token_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if request.headers.get('Authorization') != utils.get_hidden_session('auth_token'):
            return "invalid auth token", 403
        return f(*args, **kwargs)
    return decorated_function

@app.route('/api-version')
def api_version():
    return jsonify({'version': '1.0'})

#oauth stuff
@app.route('/login')
def login():
    if request.headers.get('X-Forwarded-Proto', 'http') == 'https': 
        return oauth_server.authorize(callback=url_for('authorized', _external=True, _scheme="https"))
    return oauth_server.authorize(callback=url_for('authorized', _external=True))

@app.route('/authorized')
@oauth_server.authorized_handler
def authorized(resp):
    if resp is None:
        return 'Access denied: reason=%s error=%s' % (
            request.args['error_reason'],
            request.args['error_description']
        )
    print resp
    utils.make_hidden_session('oauth', (resp['access_token'], ''))

    response = oauth_server.get(server_url + '/api/user')
    if 'objects' not in response.data or 'id' not in response.data['objects']:
        return "no user found", 404
    
    data = response.data
    print data
    utils.make_hidden_session('user_id', data['objects']['id'])
    
    auth_token = gen_salt(50)
    utils.make_hidden_session('auth_token', auth_token)
    
    session.permanent = True
                
    return jsonify({'objects': {'auth_token': auth_token}})

@app.route('/register-device-id', methods = ['POST'])
@token_required
def register_device():    
    devices = oauth_server.get(server_url + '/api/devices').data['objects']
    print devices
    print devices.__class__.__name__    
    
    user_devices = [device for device in devices if device['id'] == request.form['device_id']]
    
    if len(user_devices) != 1:
        response =  jsonify({'error': 'incorrect number of devices found for this id'})
        response.status_code = (500)
        return response
        
    user_device = user_devices[0]
    print user_device
    
    utils.make_hidden_session('device', user_device)
    return jsonify({'objects': user_device})

@oauth_server.tokengetter
def get_oauth_token():
    return utils.get_hidden_session('oauth')
 
def socketio_login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if utils.get_hidden_session('user_id') is None:
            print "not authenticated"
            return disconnect()
        return f(*args, **kwargs)
    return decorated_function
 
@app.route('/run/event', methods = ['GET', 'POST'])
@token_required
def event():
    data = json.loads(request.data)
    
    mq = current_app.config['NOCLIENT_MQ'](device_id = device.Device.id())
    mq.push(request.data)
    return jsonify({'objects': {}})

@app.route('/run/retval', methods = ['POST'])
@token_required
def return_val():
    mq = current_app.config['NOCLIENT_MQ'](key = remote_obj.return_val_key())
    mq.push(request.data)
    return jsonify({'objects': {}})
 
@socketio.on('run', namespace="/client")
@socketio_login_required
def run(message):
    if request.environ.get('wsgi.websocket'):
        print utils.get_hidden_session('device')
        device_type = utils.get_hidden_session('device')['type']
        
        from airypi import errors

        try:
            event_loop_class = device.Device.event_loop_for_type[device_type]
            event_loop = event_loop_class()
            
            while True:
                event_loop.loop()
                gevent.sleep(0)
        except errors.ExitError, e:
            print traceback.format_exc()
            pass

    return jsonify({'objects': {}})

def setup(debug = True, 
          host = 'localhost', 
          port = 8080, 
          session_interface = None, 
          session_secret = 'supersecretsessionsecret',
          client_id = None,
          client_secret = None,
          message_queue_class = message_queue.DebugMQ,
          redis_url = None):
    app.debug = debug
    
    if session_interface is not None:
        app.session_interface = session_interface
        
    app.secret_key = session_secret
    app.config['NOCLIENT_MQ'] = message_queue_class
    
    if 'REDISCLOUD_URL' in os.environ or redis_url is not None:
        from redis_queue import RedisMQ
        import redis
        
        redis_client_url = os.environ['REDISCLOUD_URL']
        if redis_url is not None:
            redis_client_url = redis_url
        print "redis url:" + redis_client_url
        app.config['NOCLIENT_MQ'] = RedisMQ
        RedisMQ.redis = redis.StrictRedis.from_url(url = redis_client_url, db = 0)
        
        app.debug = False
        
    socketio_host = host
    socketio_port = port
    
    if 'PORT' in os.environ:
        socketio_host = '0.0.0.0'
        socketio_port = int(os.environ['PORT'])
    
    #nasty hack but whatever
    oauth_server._consumer_key = client_id
    oauth_server._consumer_secret = client_secret

    socketio.run(app, host = socketio_host, port = socketio_port)

if __name__ == "__main__":
    setup()