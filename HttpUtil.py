#!/usr/bin/python
# -*- coding: utf-8 -*-

import http.client
import urllib
import json
import hashlib
import hmac

def getSign(params, secretKey):
    bSecretKey = bytes(secretKey, encoding='utf8')

    sign = ''
    for key in params.keys():
        value = str(params[key])
        sign += key + '=' + value + '&'
    bSign = bytes(sign[:-1], encoding='utf8')

    mySign = hmac.new(bSecretKey, bSign, hashlib.sha512).hexdigest()
    return mySign

def httpGet(url, resource, params=''):
    conn = http.client.HTTPSConnection(url, timeout=10)
    conn.request("GET", resource + '/' + params)
    response = conn.getresponse()
    data = response.read().decode('utf-8')
    return json.loads(data)
#[CURR_A]_[CURR_B]?group_sec=[GROUP_SEC]&range_hour=[RANGE_HOUR]
def httpGetCandle(url, resource,current_pair,GROUP_SEC,RANGE_HOUR):
    conn = http.client.HTTPSConnection(url, timeout=10)
    conn.request("GET", resource + '/' + current_pair + '?group_sec='+ str(GROUP_SEC) + '&range_hour=' + str(RANGE_HOUR))
    response = conn.getresponse()
    data = response.read().decode('utf-8')
    return json.loads(data)

def httpPost(url, resource, params, apiKey, secretKey):
     headers = {
            "Content-type" : "application/x-www-form-urlencoded",
            "KEY":apiKey,
            "SIGN":getSign(params, secretKey)
     }

     conn = http.client.HTTPSConnection(url, timeout=10)

     tempParams = urllib.parse.urlencode(params) if params else ''
     conn.request("POST", resource, tempParams, headers)
     response = conn.getresponse()
     data = response.read().decode('utf-8')
     params.clear()
     conn.close()
     return data
