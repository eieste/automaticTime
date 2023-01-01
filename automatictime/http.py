# -*- coding: utf-8 -*-
import requests
import urllib3.util


class HttpSession:

    def __init__(self, appname, config, options):
        self._app_name = appname
        self._config = config
        self._options = options

    def build_url(self, raw_path, params=None):
        url_parts = urllib3.util.parse_url(self._config.get(self._app_name).get("api_url"))
        path = raw_path.strip("/")
        org_path = url_parts.path.strip("/")
        new_url = url_parts._replace(path=f"/{org_path}/{path}")
        new_url = new_url._replace(query=params)
        return new_url

    def default_headers(self):
        return {'Content-Type': 'application/json', 'Accept': 'application/json'}

    def add_header(self, header=None):
        if header is None:
            header = {}
        request_header = self.default_headers()
        request_header["Authorization"] = f"Token token={self._config.get(self._app_name).get('api_key')}"
        request_header.update(header)
        return request_header

    def make_request(self, endpoint, method, header=None, body=None):
        request_header = self.add_header(header)
        response = requests.request(method, self.build_url(endpoint), headers=request_header, data=body)
        return response
