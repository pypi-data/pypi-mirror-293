import ctypes
import os
import platform
import subprocess
import sys

from tqdm import tqdm
import json

class Response:
    def __init__(self, status_code, text, json):
        self.status_code = status_code
        self.text = text
        self.json = json

class CurlRequest:

    def convert_json(self, text):

        try:
            return json.loads(text)
        except: return None

    def __init__(self):
        
        Linux = r"build\Debug\my_library."
        if platform.system() == "Windows":
            lib_ext = "dll"
        elif platform.system() == "Linux":
            Linux = "my_library."
            lib_ext = "so"
        else:
            raise OSError("Unsupported operating system.")

        current_dir = os.path.dirname(os.path.abspath(__file__))
        build_dir = os.path.join(current_dir, "..", "build", "Debug")
        lib_path = os.path.join(build_dir, f"my_library.{lib_ext}")
        
        try:
            self.lib = ctypes.CDLL(lib_path)
        except OSError as e:
            raise e

        self.lib.zapros.argtypes = [ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p]
        self.lib.zapros.restype = ctypes.c_char_p


    def make_request(self, url, method="get", body=None, headers=None):

        if isinstance(body, dict):
            body = json.dumps(body)
        
        if isinstance(headers, dict):
            headers = "\r\n".join([f"{key}: {value}" for key, value in headers.items()])

        body = body if body else ""
        headers = headers if headers else ""

        url_bytes = url.encode('utf-8')
        method_bytes = method.lower().encode('utf-8')
        body_bytes = body.encode('utf-8')
        headers_bytes = headers.encode('utf-8')

        response = self.lib.zapros(url_bytes, method_bytes, body_bytes, headers_bytes)
        combined_response = response.decode('utf-8')

        status_code, response_body = combined_response.split('|', 1)
        return Response(int(status_code), response_body, self.convert_json(response_body))
        
    def get(self, url, headers=None):
        return self.make_request(url, "get", headers=headers)
    
    def post(self, url, body=None, headers=None):
        return self.make_request(url, "post", body=body, headers=headers)