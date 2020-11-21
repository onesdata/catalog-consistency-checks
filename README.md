# Overview

This is a proposal for [Shopify Friday Hack Weekend](https://shopifyhackfriday.splashthat.com/).

Working with large catalogs, for example home goods store, with over 1000 products we have realized that it is a difficult task to remain the catalog consistent:
- products that the buyer cannot find because they are not in any collection
- collections that do not have products
- prices below X, for example 1 €

The purpose of the app is to help store managers know as soon as possible the inconsistencies in the store's catalog in order to correct them and not lose sales.

## Get started

To make it easy to get started:
- we have created a development store: https://hack-friday.myshopify.com/ (ask @j-plou or @valentinboyanov for invitation)
- we have created a private app: to make it easy, for now the credentials are harcoded in the [Makefile](Makefile) and can be make ready to use by running `make gather_creds`
- we have created a python web application based on tornado that retrieve from the Store (using the private app) all products: [app/web_ui.py](app/web_ui.py)
- we have deployed the web application in heroku: https://catalog-consistency-checks.herokuapp.com/

You can run the web application locally by following the instructions here: [Run web app locally](#run-web-app-locally)

## Usage

* `make check` sets working env with requirements
* `make gather_creds` sets remote Shopify credentials
* `make test` runs tests
* `make fmt` runs formatters

## Run web app locally

1. Prepare environment: `make env_ok`
2. Prepare credentials: `make gather_creds`
3. Run web app:
    ```
    APP_API_URL=$(cat in/APP_API_URL) \
    APP_API_PASSWORD=$(cat in/APP_API_PASSWORD) \
    APP_API_KEY=$(cat in/APP_API_KEY) \
    env/bin/python app/web_ui.py
    ```

4. Access web app from your browser at: http://127.0.0.7:8000/

## Get all products via CLI

1. Prepare environment: `make env_ok`
2. Prepare credentials: `make gather_creds`
3. Get all products:
    ```
    APP_API_URL=$(cat in/APP_API_URL) \
    APP_API_PASSWORD=$(cat in/APP_API_PASSWORD) \
    APP_API_KEY=$(cat in/APP_API_KEY) \
    env/bin/python app/shopify_api.py
    ```

## Check active product weight

```
APP_API_URL=$(cat in/APP_API_URL) \
APP_API_PASSWORD=$(cat in/APP_API_PASSWORD) \
APP_API_KEY=$(cat in/APP_API_KEY) \
env/bin/python app/checks.py
```

## Heroku deploy

The web app is available at https://catalog-consistency-checks.herokuapp.com/

It is an application based on `heroku/python` buildpack whose environment can be configured by running `make set_heroku_config_vars` and for now the deploy is manual, executed by @valentinboyanov
