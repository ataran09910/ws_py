import random
import re
import string

import flask
from flask import abort

from core import errors


class Validation:
    def __init__(self):
        self.short_codes = []
        self.response = flask.Response("Location Header")

    def find_shortcode_in_db(self, short_code):
        for code in self.short_codes:
            if code == short_code:
                return True

    def check_if_url_empty(self, url):
        if not url:
            abort(400, errors.BAD_URL)
        else:
            return url

    def generate_code_if_empty(self, input_code):
        mask = string.ascii_letters + "_" + string.digits
        code_length = 6
        if not input_code:
            out = ''.join((random.choice(mask) for _ in range(code_length)))
        else:
            out = input_code
        self.validate_code(out)
        self.check_if_already_exists(out)
        self.short_codes.append(out)
        return out

    def check_if_already_exists(self, input_code):
        if self.find_shortcode_in_db(input_code):
            abort(409, errors.CONFLICT)

    def validate_code(self, input_code):
        if not re.match(r'^[a-zA-Z0-9_]{6}$', input_code):
            abort(412, errors.PRECONDITION_FAILED)
