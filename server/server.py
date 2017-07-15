from tornado import websocket
import tornado.ioloop
import threading
import Queue

q = Queue.Queue()


class EchoWebSocket(websocket.WebSocketHandler):
    def check_origin(self, origin):
        return True

    def open(self):
        print "Websocket Opened"

    def on_message(self, message):
        #print(u"message %s" % message)
        self.write_message(u"You said: %s" % message)
        q.put(message)

    def on_close(self):
        print "Websocket closed"


def start():
    application = tornado.web.Application([(r"/", EchoWebSocket),])
    application.listen(9001)

    t = threading.Thread(target=tornado.ioloop.IOLoop.instance().start)
    t.daemon = True
    t.start()


def stop():
    tornado.ioloop.IOLoop.instance().stop()
