import base64
import os
import re
from typing import Any, Dict, Iterable, Optional

import requests


def get_all_products(api_url: str, api_key: str, api_password: str) -> Iterable[Any]:
    authorization_str = "{0}:{1}".format(api_key, api_password)
    authorization_bytes = authorization_str.encode("ascii")
    authorization_base64 = base64.b64encode(authorization_bytes)
    headers = {
        "Authorization": "Basic {0}".format(authorization_base64.decode("ascii")),
        "content-type": "application/json",
    }

    products_url = os.path.join(api_url, "products.json")
    response = requests.get(products_url, headers=headers)

    return products_iter(response, headers)


def products_iter(
    response: Optional[requests.models.Response], headers: Dict
) -> Iterable[Any]:
    while response is not None:
        for product in response.json()["products"]:
            yield product

        response = get_next_response(response, headers)


def get_next_response(
    response: requests.models.Response, headers: Dict
) -> Optional[requests.models.Response]:
    if "Link" in response.headers:
        links: Dict = get_pagination_links(response.headers["Link"])
        if "next" in links:
            return requests.get(links["next"], headers=headers)
    return None


def get_pagination_links(links: str) -> dict:
    all_links = {}
    links_dict = links.split(",")
    for link in links_dict:
        pattern = '<(.*)>; rel="(\w*)"'
        match = re.search(pattern, link)
        if match:
            all_links[match.group(2)] = match.group(1)
    return all_links


if __name__ == "__main__":
    env = os.environ
    api_url: str = env["APP_API_URL"]
    api_key: str = env["APP_API_KEY"]
    api_password: str = env["APP_API_PASSWORD"]

    products = list(get_all_products(api_url, api_key, api_password))

    print(products)
