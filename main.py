# -*- coding: utf-8 -*-
"""
Require '.headers' file' - Request headers
"""
import time

ROOT_URL = 'php.tsacerof/2dehcac/XAJA/ur.tropsrebyc.www//:ptth'[::-1]
HEADERS_FILE = '.headers'
FORECAST_ID_XPATH = '//div[@class="forecast"]/@data-mid'
FORECAST_VOTES_XPATH = '//div[@class="forecast-votes"]/@data-votes'


def make_post(headers_dict=None, params_str=None):
    import requests

    if params_str:
        url = '{0}?params={1}'.format(ROOT_URL, params_str)
        return requests.post(url, headers=headers_dict)
    return requests.post(ROOT_URL, headers=headers_dict)


def parsed_to_params(parsed):
    """
    Convert structured dictionary to {id: choice} dict
    :param parsed: Structured dictionary
    :return: {id: choice}
    """
    id_ = parsed.get('id')
    choice = get_choice(parsed)
    return {id_: choice}


def get_choice(parsed):
    """
    Get choice based on 'votes' values
    :param parsed: Structured dictionary
    :return: "1" or "2"
    """
    votes = parsed.get('votes', {})
    left = votes.get('left', 0)
    right = votes.get('right', 0)
    if left > right:
        return "1"
    else:
        return "2"


def parse_response(content):
    """
    Parse HTML response to {'id': 'id_val', 'votes': {"all":64,"left":17,"right":47}} dictionary
    :param content: HTML content
    :return: structured dictionary
    """
    from lxml import html
    import json
    tree = html.fromstring(content)
    f_id = tree.xpath(FORECAST_ID_XPATH)
    f_votes = tree.xpath(FORECAST_VOTES_XPATH)
    result = {}
    if f_id and 0 < len(f_id):
        result.update({'id': f_id[0]})
    if f_votes and 0 < len(f_votes):
        result.update({'votes': json.loads(f_votes[0])})
    return result


def quote_params(params):
    """
    Transform params from dictionary {"191677": "1"} into custom encoded string '{%22191677%22:%221%22}'
    :param params: dictionary
    :return: encoded string
    """
    import urllib
    import json

    dumps = json.dumps(params, separators=(',', ':'))  # no whitespace after colon
    return urllib.quote(dumps, "{:}")


def get_headers(headers_file=HEADERS_FILE):
    """
    Read and parse 'headers' dictionary from HEADERS_FILE
    :return: 'headers' dictionary
    """
    headers = {}
    with open(headers_file, mode='r') as f:
        for line in f.readlines():
            if line:
                split = line.split(':', 1)
                left = split[0]
                right = split[1].lstrip(' ').rstrip('\n')  # remove leading whitespace and trailing \n
                headers.update({left: right})
    return headers


if __name__ == '__main__':
    import sys
    headers = get_headers()
    response = make_post(headers_dict=headers)
    if response.ok:
        parsed = parse_response(response.content)
        params = parsed_to_params(parsed)
        qs = quote_params(params)
    else:
        sys.exit('Response is not OK')
    while 1:
        while 1:
            response = make_post(headers_dict=headers, params_str=qs)
            if response.ok:
                parsed = parse_response(response.content)
                if not parsed:
                    break
                params = parsed_to_params(parsed)
                qs = quote_params(params)
                print 'Processed 1 item'
        print 'Waiting...'
        time.sleep(120)
