import datetime
import time
from flask import *
from utilities.common import utc_now_ts as utcnow


log_app = Blueprint('log_app', __name__, template_folder='templates')


# function that execute before view function
# Like Flask.before_request()
@log_app.before_app_request
def start_timer():
    g.start = time.time()


@log_app.after_app_request
def log_request(response):
    if request.path == '/favicon.ico':
        return response
    elif request.path.startswith('/static'):
        return response

    now = time.time()
    duration = round(now - g.start, 2)
    dt = datetime.datetime.fromtimestamp(now)
    timestamp = utcnow()

    ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    host = request.host.split(':', 1)[0]
    args = dict(request.args)

    log_params = [
        ('method', request.method),
        ('path', request.path),
        ('status', response.status_code),
        ('duration', duration),
        ('time', timestamp),
        ('ip', ip),
        ('host', host),
        ('params', args)
    ]

    request_id = request.headers.get('X-Request-ID')
    if request_id:
        log_params.append(('request_id', request_id, 'yellow'))

    parts = []
    for name, value in log_params:
        part = "{}={}".format(name, value)
        parts.append(part)
    line = " ".join(parts)

    current_app.logger.info(line)

    return response
