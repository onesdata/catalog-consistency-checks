import os

import tornado.httpserver
import tornado.ioloop
import tornado.web
from tornado.options import define, options

from checks import get_products_outside_range
from shopify_api import get_all_products

define("port", default=8000, help="run on the given port", type=int)


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("<h1>Checks</h1>")
        self.write("<ul>")
        self.write(
            '<li><a href="/checks/product-weight">The weight of all active products is between 3 and 6 kg</a></li>'
        )
        self.write("</ul>")


class ProductsHandler(tornado.web.RequestHandler):
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
                "<strong>Qty:</strong> " + str(p["variants"][0]["inventory_quantity"])
            )
            self.write("</li>")
        self.write("</ul>")


class ActiveProductsWeight(tornado.web.RequestHandler):
    def get(self):
        products = list(get_all_products(api_url, api_key, api_password))
        products_outside_range = get_products_outside_range(products, 3.0, 6.0)

        if len(products_outside_range) > 0:
            self.write(
                '<p style="color: red">Products whose weight is outside the expected range (3.0 - 6.0 kg): {0}</p>'.format(
                    products_outside_range
                )
            )
        else:
            self.write(
                '<p style="color: green">All products are in the expected range (3.0 - 6.0 kg).</p>'
            )


if __name__ == "__main__":
    env = os.environ
    api_url: str = env["APP_API_URL"]
    api_key: str = env["APP_API_KEY"]
    api_password: str = env["APP_API_PASSWORD"]

    tornado.options.parse_command_line()
    application = tornado.web.Application(
        [
            (r"/", MainHandler),
            (r"/checks/product-weight", ActiveProductsWeight),
            (r"/products", ProductsHandler),
        ],
        api_url=api_url,
        api_key=api_key,
        api_password=api_password,
    )
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.current().start()
