import os
from typing import List, Tuple

from shopify_api import get_all_products

if __name__ == "__main__":
    env = os.environ
    api_url: str = env["APP_API_URL"]
    api_key: str = env["APP_API_KEY"]
    api_password: str = env["APP_API_PASSWORD"]

    products = list(get_all_products(api_url, api_key, api_password))
    variants: List[Tuple[str, str, float]] = []

    for p in products:
        for v in p["variants"]:
            variants.append((p["handle"], v["id"], v["weight"]))

    min_weight_kg: float = 3.0
    max_weight_kg: float = 6.0

    products_outside_range: List = []
    for handle, id, weight in variants:
        if weight > max_weight_kg or weight < min_weight_kg:
            products_outside_range.append((handle, id, weight))

    if len(products_outside_range) > 0:
        raise Exception(
            "Products whose weight is outside the expected range ({0} - {1} kg): {2}".format(
                min_weight_kg, max_weight_kg, products_outside_range
            )
        )
