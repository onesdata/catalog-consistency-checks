import os

import tornado.httpserver
import tornado.ioloop
import tornado.web
from tornado.options import define, options

from checks import get_products_outside_range, get_products_with_insufficient_images
from shopify_api import get_all_products

define("port", default=8000, help="run on the given port", type=int)


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("<h1>Checks</h1>")
        self.write("<ul>")
        self.write(
            '<li>The weight of all active products is between 0.3 and 6.0 kg: <a href="/checks/product-weight">run check</a></li>'
        )
        self.write(
            '<li>All active products have at least 3 images: <a href="/checks/product-images">run check</a></li>'
        )
        self.write("</ul>")

        self.write("<style>\
            body { \
                font-family: -apple-system, BlinkMacSystemFont, San Francisco, Segoe UI, Roboto, Helvetica Neue, sans-serif;\
                font-size: 14px;\
                } \
            h1 {\
                font-size: 28px;\
                font-weight: 600;\
            }\
            a {\
                text-decoration: none;\
            }\
            a:hover {\
                text-decoration: underline;\
            }\
            ul {\
                list-style: none;\
            }\
            li {\
                margin-bottom: 20px;\
            }\
            </style>")


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
                "<strong>Qty:</strong> " + str(p["variants"][0]["inventory_quantity"]) + "<br />"
            )
            self.write("<strong>Weight:</strong> " + str(p["variants"][0]["weight"]))
            self.write("</li>")
        self.write("</ul>")        
        self.write('<a href="/">Back</a>')

        self.write("<style>\
            body { \
                font-family: -apple-system, BlinkMacSystemFont, San Francisco, Segoe UI, Roboto, Helvetica Neue, sans-serif;\
                font-size: 14px;\
                } \
            h1 {\
                font-size: 28px;\
                font-weight: 600;\
            }\
            a {\
                text-decoration: none;\
            }\
            a:hover {\
                text-decoration: underline;\
            }\
            ul {\
                list-style: none;\
            }\
            li {\
                margin-bottom: 20px;\
            }\
            </style>")


class ActiveProductsWeight(tornado.web.RequestHandler):
    def get(self):
        products = list(get_all_products(api_url, api_key, api_password))
        products_outside_range = get_products_outside_range(products, 0.3, 6.0)

        if len(products_outside_range) > 0:
            self.write('<p>Check status: <span style="color: red">failed</span></p>')
            self.write(
                "<p>Products whose weight is outside the expected range (0.3 - 6.0 kg):</p>"
            )
            self.write("<ul>")
            for p_handle, v_id, v_weight in products_outside_range:
                self.write(
                    "<li>Product handle: {0}, Variant id: {1}, Variant weight: {2}</li>".format(
                        p_handle, v_id, v_weight
                    )
                )
            self.write("</ul>")
        else:
            self.write('<p>Check status: <span style="color: green">passed</span></p>')
            self.write(
                '<p style="color: green">All products are in the expected range (0.3 - 6.0 kg).</p>'
            )

        self.write('<a href="/">Back</a>')

        self.write("<style>\
            body { \
                font-family: -apple-system, BlinkMacSystemFont, San Francisco, Segoe UI, Roboto, Helvetica Neue, sans-serif;\
                font-size: 14px;\
                } \
            h1 {\
                font-size: 28px;\
                font-weight: 600;\
            }\
            a {\
                text-decoration: none;\
            }\
            a:hover {\
                text-decoration: underline;\
            }\
            ul {\
                list-style: none;\
            }\
            li {\
                margin-bottom: 20px;\
            }\
            </style>")

class ActiveProductsImages(tornado.web.RequestHandler):
    def get(self):
        products = list(get_all_products(api_url, api_key, api_password))
        products_few_images = get_products_with_insufficient_images(products, 3)

        if len(products_few_images) > 0:
            self.write('<p>Check status: <span style="color: red">failed</span></p>')
            self.write("<p>Active products that have less than 3 images:</p>")
            self.write("<ul>")
            for handle, images_num in products_few_images:
                self.write(
                    "<li>Product handle: {0}, Images num: {1}</li>".format(
                        handle, images_num
                    )
                )
            self.write("</ul>")
        else:
            self.write('<p>Check status: <span style="color: green">passed</span></p>')
            self.write(
                '<p style="color: green">All active products have at least 3 images.</p>'
            )

        self.write('<a href="/">Back</a>')
        
        self.write("<style>\
            body { \
                font-family: -apple-system, BlinkMacSystemFont, San Francisco, Segoe UI, Roboto, Helvetica Neue, sans-serif;\
                font-size: 14px;\
                } \
            h1 {\
                font-size: 28px;\
                font-weight: 600;\
            }\
            a {\
                text-decoration: none;\
            }\
            a:hover {\
                text-decoration: underline;\
            }\
            ul {\
                list-style: none;\
            }\
            li {\
                margin-bottom: 20px;\
            }\
            </style>")


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
            (r"/checks/product-images", ActiveProductsImages),
            (r"/products", ProductsHandler),
        ],
        api_url=api_url,
        api_key=api_key,
        api_password=api_password,
    )
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.current().start()
