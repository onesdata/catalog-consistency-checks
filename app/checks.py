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


def get_products_with_insufficient_images(
    products: List, min_image_num: int
) -> List[Tuple[str, int]]:
    res: List[Tuple[str, int]] = []

    active_products = [p for p in products if p["status"] == "active"]
    for p in active_products:
        images_num = len(p["images"])
        if images_num < min_image_num:
            res.append((p["handle"], images_num))

    return res


if __name__ == "__main__":
    env = os.environ

    api_url: str = env["APP_API_URL"]
    api_key: str = env["APP_API_KEY"]
    api_password: str = env["APP_API_PASSWORD"]

    parser = argparse.ArgumentParser()

    parser.add_argument("check", choices=["products-weight", "products-images"])

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
    elif args.check == "products-images":
        products = list(get_all_products(api_url, api_key, api_password))
        products_few_images = get_products_with_insufficient_images(products, 5)

        if len(products_few_images) > 0:
            raise Exception(
                "Active products that have less than 3 images: {0}".format(
                    products_few_images
                )
            )
    else:
        raise Exception("check not implemented: {0}".format(args.check))
