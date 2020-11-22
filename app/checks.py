import argparse
import os
from typing import List, Tuple

from shopify_api import get_all_products


def get_products_outside_range(
    products: List, min_weight_kg: float, max_weight_kg: float
) -> List[Tuple[str, str, str]]:

    res: List[Tuple[str, str, str]] = []

    active_products = [p for p in products if p["status"] == "active"]
    for p in active_products:
        for v in p["variants"]:
            if v["weight"] > max_weight_kg or v["weight"] < min_weight_kg:
                res.append((p["handle"], v["id"], v["weight"]))

    return res


if __name__ == "__main__":
    env = os.environ

    api_url: str = env["APP_API_URL"]
    api_key: str = env["APP_API_KEY"]
    api_password: str = env["APP_API_PASSWORD"]

    parser = argparse.ArgumentParser()

    parser.add_argument("check", choices=["products-weight"])

    args = parser.parse_args()

    if args.check == "products-weight":
        products = list(get_all_products(api_url, api_key, api_password))
        products_outside_range = get_products_outside_range(products, 0.3, 6.0)

        if len(products_outside_range) > 0:
            raise Exception(
                "Products whose weight is outside the expected range (0.3 - 6.0 kg): {0}".format(
                    products_outside_range
                )
            )
    else:
        raise Exception("cmd not implemented: {0}".format(args.cmd))
