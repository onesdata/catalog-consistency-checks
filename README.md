# Overview

This is our proposal for [Shopify Friday Hack Weekend](https://shopifyhackfriday.splashthat.com/).

Working with large catalogs, for example home goods store, with over 1000 products we have realized that it is a difficult task to remain the catalog consistent:
- products that the buyer cannot find because they are not in any collection
- collections that do not have products
- prices below X, for example 1 €

The purpose of the app is to help store managers know as soon as possible the inconsistencies in the store's catalog in order to correct them and not lose sales.

## Usage

* `make check` sets working env with requirements
* `make gather_creds` sets remote Shopify credentials
* `make test` runs tests
* `make fmt` runs formatters

## Run web server

```
APP_API_URL=$(cat in/APP_API_URL) \
APP_API_PASSWORD=$(cat in/APP_API_PASSWORD) \
APP_API_KEY=$(cat in/APP_API_KEY) \
env/bin/python app/web_ui.py
```

Access server from your browser at: http://127.0.0.7:8000/

## Get all products

```
APP_API_URL=$(cat in/APP_API_URL) \
APP_API_PASSWORD=$(cat in/APP_API_PASSWORD) \
APP_API_KEY=$(cat in/APP_API_KEY) \
env/bin/python app/shopify_api.py
```


