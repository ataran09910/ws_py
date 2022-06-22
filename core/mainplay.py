from flask import Flask, request, Response, jsonify, abort

from core import errors
from core.validation import Validation


class MainPlay:
    def __init__(self, host='127.0.0.1', port=5000, debug=True):
        self.debug = debug
        self.port = port
        self.host = host
        self.app = Flask(__name__)
        self.response = Response("Location Header")

    def run(self):
        self.app.run(debug=self.debug, port=self.port, host=self.host)
        pass


play = MainPlay()
app = play.app
validate = Validation()


@app.route('/about', methods=['GET'])
def home():
    return "<h1>This is my first web service written on Python ever</h1>" \
           "<p>Lets see what happens next :) </p>"


@app.route('/shorten', methods=['POST'])
def shorten():
    data = request.get_json()
    validate.check_if_url_empty(data['url'])
    code = data['shortcode']
    play.response.headers['location'] = "/shorten"
    return jsonify({'shortcode': validate.generate_code_if_empty(code)}), 201


@app.route('/<shortcode>/stats', methods=['GET'])
def get_stats(shortcode):
    if validate.find_shortcode_in_db(shortcode):
        return request.args, 200


@app.route('/codes', methods=['GET'])
def get_all_codes():
    return jsonify(validate.short_codes)


@app.route('/<shortcode>', methods=['GET'])
def get_location_header(shortcode):
    if validate.find_shortcode_in_db(shortcode):
        return jsonify(play.response.headers['location']), 302
    else:
        abort(404, errors.NOT_FOUND)


if __name__ == '__main__':
    play.run()
