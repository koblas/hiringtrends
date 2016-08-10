#!/usr/bin/env python

import tornado.ioloop
from tornado.options import options, define
from app import application

define("port", default=8888)

if __name__ == '__main__':
    tornado.options.parse_command_line()

    app = application.Application()
    app.listen(options.port)
    print("Listening on port %s" % options.port)
    tornado.ioloop.IOLoop.current().start()
