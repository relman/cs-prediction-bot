# -*- coding: utf-8 -*-
import unittest


class TestMain(unittest.TestCase):
    def test_get_headers(self):
        # assign
        test_file = '.test_headers'
        host, host_value = 'Host', 'test.com'
        cl, cl_value = 'Content-Length', '15'
        with open(test_file, 'w') as f:
            f.write(host + ': ' + host_value + '\n')
            f.write(cl + ': ' + cl_value + '\n')
        # assert
        from main import get_headers
        headers = get_headers(test_file)
        self.assertEqual(headers.get(host), host_value)
        self.assertEqual(headers.get(cl), cl_value)
        # cleanup
        import os
        os.remove(test_file)

    def test_quote_params(self):
        obj = {"191677": "1"}
        expected = '{%22191677%22:%221%22}'
        from main import quote_params
        result = quote_params(obj)
        self.assertEqual(expected, result)

    def test_parse_response(self):
        with open('test_parse.html') as f:
            text = f.read()
        from main import parse_response
        result = parse_response(text)
        self.assertEqual(result['id'], '860')
        self.assertTrue(result['votes'])
        self.assertEqual(result['votes']['all'], 64)

    def test_get_choice_1(self):
        from main import get_choice
        result = get_choice({'votes': {'left': 20, 'right': 11}})
        self.assertEqual('1', result)

    def test_get_choice_2(self):
        from main import get_choice
        result = get_choice({'votes': {'left': 9, 'right': 35}})
        self.assertEqual('2', result)

    def test_get_choice_empty(self):
        from main import get_choice
        result = get_choice({})
        self.assertEqual('2', result)

    def test_parsed_to_params(self):
        from main import parsed_to_params
        val = '123'
        result = parsed_to_params({'id': val, 'votes': {}})
        self.assertEqual({val: "2"}, result)


if __name__ == '__main__':
    unittest.main()
