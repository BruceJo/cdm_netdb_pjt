import sys
import os
import hashlib
import hmac
import base64
import requests
import json
import time
from flask import Flask, request, jsonify
import psycopg2
from psycopg2.extras import RealDictCursor
from datetime import datetime

ACCESS_KEY = "mYUP1ZqESUOpjyOokWC8"
SECRET_KEY = "31scunD8FAtSTqU92X2DYFsi1UaiEbQ5qrTxi2aM"
BASE_URL = "https://ncloud.apigw.gov-ntruss.com"

def create_signature(method, api_url, timestamp, access_key):
    message = f"{method} {api_url}\n{timestamp}\n{access_key}"
    message = bytes(message, 'UTF-8')
    secret_key_bytes = bytes(SECRET_KEY, 'UTF-8')
    signing_key = base64.b64encode(hmac.new(secret_key_bytes, message, digestmod=hashlib.sha256).digest())
    return signing_key.decode('UTF-8')

def send_request(method, api_url, timestamp):
    signature = create_signature(method, api_url, timestamp, ACCESS_KEY)
    http_header = {
        'x-ncp-apigw-timestamp': timestamp,
        'x-ncp-iam-access-key': ACCESS_KEY,
        'x-ncp-apigw-signature-v2': signature
    }
    full_url = BASE_URL + api_url
    if method == "GET":
        response = requests.get(full_url, headers=http_header)
    elif method == "POST":
        response = requests.post(full_url, headers=http_header)
    return response

def get_server_list(timestamp):
    method = "GET"
    api_url = f"/vserver/v2/getAccessControlGroupRuleList?regionCode=KR&accessControlGroupNo={39168}&responseFormatType=json"
    return send_request(method, api_url, timestamp)

timestamp = str(int(time.time() * 1000))
response = get_server_list(timestamp)
json_data = response.text
print(json_data)