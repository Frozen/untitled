from replace import celery, connection, channel
import ujson

#connection ,channel = pika_connect()


def callback(ch, method, properties, body):
    data = ujson.loads(body)
    func = celery.functions[data['func_name']](*data['args'])
    print globals()
    print " [x] Received ", ch, method, properties, body

channel.basic_consume(callback,
    queue='maxpark',
    no_ack=True)

channel.start_consuming()

