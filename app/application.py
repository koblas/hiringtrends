import tornado.web
import datetime
from hiring.util import MONTHS
from jinja2 import Environment, PackageLoader

def get_months():
    months = []
    today = datetime.date.today()

    for year in range(today.year, 2012, -1):
        for month in range(12, 1, -1):
            dval = datetime.date(year, month, 1)
            if dval > today:
                continue
            months.append((dval.strftime("%Y/%B.html").lower(), dval.strftime("%B %Y")))

    return months


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        tmpl = self.application.jenv.get_template('index.html')

        variables = {
            'months': get_months(),
        }

        self.write(tmpl.render(**variables))

class PostHandler(tornado.web.RequestHandler):
    def get(self, year, month):
        date = datetime.date(int(year), MONTHS[month], 1)

        print("Getting POST ", date)

        tmpl = self.application.jenv.get_template('post.html')

        variables = {
            'data_filename': '%(year)d/data-%(year)d%(mnum)02d01.js' % { 'year' : date.year, 'mnum' : date.month },
            'month': date.strftime('%B'),
            'year': date.year,
            'date': date.day,
            'day': date.strftime('%A'),
            'months': get_months(),
        }

        self.write(tmpl.render(**variables))

class Application(tornado.web.Application):
    def __init__(self):
        settings = {
            'static_path' : 'static',
        }

        routes = [
            (r'/', MainHandler),
            (r'/data/(\d+/data-\d+.js)', tornado.web.StaticFileHandler, { 'path': settings['static_path'] }),
            (r'/js/([^/]+.js)', tornado.web.StaticFileHandler, { 'path': settings['static_path'] }),
            (r'/(\d+)/(\w+).html', PostHandler),
        ]

        options = {
        }

        self.jenv = Environment(loader=PackageLoader('app'))

        super().__init__(routes, **options)
