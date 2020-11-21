import os

import tornado.httpserver
import tornado.ioloop
import tornado.web

import shopify_api


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        products = list(
            shopify_api.get_all_products(
                self.settings["api_url"],
                self.settings["api_key"],
                self.settings["api_password"],
            )
        )
        for p in products:
            self.write(str(p["id"]))


def main(api_url: str, api_key: str, api_password: str):
    application = tornado.web.Application(
        [(r"/", MainHandler)],
        api_url=api_url,
        api_key=api_key,
        api_password=api_password,
    )
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(8000)
    tornado.ioloop.IOLoop.current().start()


if __name__ == "__main__":
    env = os.environ
    api_url: str = env["APP_API_URL"]
    api_key: str = env["APP_API_KEY"]
    api_password: str = env["APP_API_PASSWORD"]

    main(api_url, api_key, api_password)
