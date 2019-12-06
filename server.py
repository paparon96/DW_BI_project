from gevent.pywsgi import WSGIServer
from air_app import app

http_server = WSGIServer(('', 8050), app.server)
http_server.serve_forever()
