import flask

from proxies_scraper.main import get_proxies

app = flask.Flask(__name__)


@app.route("/proxies", methods=["GET"])
def proxies():
    # Extract query parameters
    country_codes_filter = flask.request.args.get("country_codes_filter")
    anonymity_filter = flask.request.args.get("anonymity_filter")
    https_filter = flask.request.args.get("https_filter")

    # Call your module's function to get the list of proxies
    proxy_list = get_proxies(country_codes_filter, anonymity_filter, https_filter)

    # Convert the list to JSON and return it
    return flask.jsonify({"proxies": proxy_list})


if __name__ == "__main__":
    app.run(debug=True)
