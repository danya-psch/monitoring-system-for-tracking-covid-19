from requests_to_api import *
# from flask import Flask

# app = Flask(__name__)

# def get_hit_count():
#     retries = 5
#     while True:
#         try:
#             return r.incr('hits')
#         except redis.exceptions.ConnectionError as exc:
#             if retries == 0:
#                 raise exc
#             retries -= 1
#             time.sleep(0.5)
#
#
# @app.route('/')
# def hello():
#     count = get_hit_count()
#     return 'Hello from Docker! I have been seen {} times.\n'.format(count)
from redis_server import RedisServer
from view import View

if __name__ == '__main__':
    # a = RedisServer()
    view = View()

