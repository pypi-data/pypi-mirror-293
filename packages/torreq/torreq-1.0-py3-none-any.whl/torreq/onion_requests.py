import requests
from stem import Signal
from stem.control import Controller
from socksipy import socket
from urllib.parse import urlparse

class OnionRequests:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.controller = Controller.from_port(port=9051)
            cls._instance.controller.authenticate()
            cls._instance.tor_session = requests.Session()
            cls._instance.tor_session.proxies = {'http': 'socks5h://localhost:9050', 'https': 'socks5h://localhost:9050'}
            cls._instance.normal_session = requests.Session()
        return cls._instance

    def request(self, method, url, **kwargs):
        parsed_url = urlparse(url)
        if parsed_url.netloc.endswith('.onion'):
            try:
                response = self.tor_session.request(method, url, **kwargs)
                return response
            except requests.exceptions.RequestException as e:
                self.controller.signal(Signal.NEWNYM)
                response = self.tor_session.request(method, url, **kwargs)
                return response
        else:
            return self.normal_session.request(method, url, **kwargs)

    def get(self, url, **kwargs):
        return self.request('GET', url, **kwargs)

    def post(self, url, **kwargs):
        return self.request('POST', url, **kwargs)

    def put(self, url, **kwargs):
        return self.request('PUT', url, **kwargs)

    def delete(self, url, **kwargs):
        return self.request('DELETE', url, **kwargs)

    def head(self, url, **kwargs):
        return self.request('HEAD', url, **kwargs)

    def options(self, url, **kwargs):
        return self.request('OPTIONS', url, **kwargs)

    def patch(self, url, **kwargs):
        return self.request('PATCH', url, **kwargs)

    def connect(self, url, **kwargs):
        return self.request('CONNECT', url, **kwargs)

    def trace(self, url, **kwargs):
        return self.request('TRACE', url, **kwargs)

onion = OnionRequests()

def get(url, **kwargs):
    return onion.get(url, **kwargs)

def post(url, **kwargs):
    return onion.post(url, **kwargs)

def put(url, **kwargs):
    return onion.put(url, **kwargs)

def delete(url, **kwargs):
    return onion.delete(url, **kwargs)

def head(url, **kwargs):
    return onion.head(url, **kwargs)

def options(url, **kwargs):
    return onion.options(url, **kwargs)

def patch(url, **kwargs):
    return onion.patch(url, **kwargs)

def connect(url, **kwargs):
    return onion.connect(url, **kwargs)

def trace(url, **kwargs):
    return onion.trace(url, **kwargs)
