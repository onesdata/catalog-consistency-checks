import os

import tornado.httpserver
import tornado.ioloop
import tornado.web
from tornado.options import define, options

from shopify_api import get_all_products

define("port", default=8000, help="run on the given port", type=int)


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        products = list(
            get_all_products(
                self.settings["api_url"],
                self.settings["api_key"],
                self.settings["api_password"],
            )
        )
        self.write("<ul>")
        for p in products:
            self.write("<li>")
            self.write("<strong>Product:</strong> " + p["title"] + "<br />")
            self.write("<strong>SKU:</strong> " + p["variants"][0]["sku"] + "<br />")
            self.write(
                "<strong>Price:</strong> " + p["variants"][0]["price"] + "<br />"
            )
            self.write(
                "<strong>Qty:</strong> "
                + str(p["variants"][0]["inventory_quantity"])
                + "<br />"
            )
            self.write("</li>")
        self.write("</ul>")


if __name__ == "__main__":
    env = os.environ
    api_url: str = env["APP_API_URL"]
    api_key: str = env["APP_API_KEY"]
    api_password: str = env["APP_API_PASSWORD"]

    tornado.options.parse_command_line()
    application = tornado.web.Application(
        [(r"/", MainHandler)],
        api_url=api_url,
        api_key=api_key,
        api_password=api_password,
    )
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.current().start()
