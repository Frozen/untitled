#!/usr/bin/python
from functools import wraps, partial
import pika
import ujson
#from test import my_func_name

#my_func_name


def pika_connect():
    connection = pika.BlockingConnection(pika.ConnectionParameters(
        host='localhost'))
    channel = connection.channel()

    channel.queue_declare(queue='maxpark')
    return connection, channel

connection, channel = pika_connect()

def _publish(data):
    message = ujson.encode(data)
    channel.basic_publish(exchange='', routing_key='maxpark', body=message)


def send(func_name, args=(), kwargs=None):
    data = {
        'func_name' : func_name,
        'args' : args,
        'kwargs' : kwargs
    }
    _publish(data)

def _task(f):
    Celery.functions[f.__name__] = f
    f.apply_async = partial(send, f.__name__)
    @wraps(f)
    def ret(*args, **kwargs):
        return f(*args, **kwargs)
    return ret

class Celery(object):

    functions = {}

    def task(self, *args, **kwargs):
        return _task

celery = Celery()