import unittest

from flask import Flask
from numpy.compat import basestring
from werkzeug.exceptions import BadRequest, Conflict, PreconditionFailed

from core.mainplay import MainPlay
from core.validation import Validation


class TestSuite(unittest.TestCase):
    def test_validation_class(self):
        validate = Validation()
        with self.assertRaises(BadRequest):
            validate.check_if_url_empty("")
        self.assertIsInstance(validate.check_if_url_empty("test.com"), basestring)
        self.assertTrue(not validate.short_codes)
        test_code = "abc123"
        validate.short_codes.append(test_code)
        self.assertTrue(validate.find_shortcode_in_db(test_code))
        self.assertIsNone(validate.find_shortcode_in_db("nocode"))
        self.assertIsInstance(validate.generate_code_if_empty(""), basestring)
        self.assertIsNotNone(validate.generate_code_if_empty(""))
        with self.assertRaises(Conflict):
            validate.generate_code_if_empty(test_code)
        with self.assertRaises(PreconditionFailed):
            validate.validate_code("tescode")

    def test_webservice_core(self):
        ws_instance = MainPlay()
        self.assertIsInstance(ws_instance.app, Flask)
        self.assertIsInstance(ws_instance.debug, bool)
        self.assertIsInstance(ws_instance.host, basestring)
        self.assertIsInstance(ws_instance.port, int)
