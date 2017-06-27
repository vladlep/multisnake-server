from tornado import websocket
import tornado.ioloop

class EchoWebSocket(websocket.WebSocketHandler):
    def check_origin(self, origin):
        return True

    def open(self):
        print "Websocket Opened"

    def on_message(self, message):
        print(u"message %s" % message)
        self.write_message(u"You said: %s" % message)

    def on_close(self):
        print "Websocket closed"

application = tornado.web.Application([(r"/", EchoWebSocket),])

if __name__ == "__main__":
    application.listen(9000)
    tornado.ioloop.IOLoop.instance().start()
