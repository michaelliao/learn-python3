#!/usr/bin/env python3
# -*- coding: utf-8 -*-

r'''
learning.py

A Python 3 tutorial from https://www.liaoxuefeng.com

Usage:

python3 learning.py
'''

# check #######################################################################

import sys
from datetime import datetime

CERT_EXPIRES = '2019-07-07'

def check_version():
    v = sys.version_info
    if v.major == 3 and v.minor >= 5:
        return
    print('Your current python is %d.%d. Please use Python 3.6.' % (v.major, v.minor))
    exit(1)

def check_cert():
    today = datetime.now().strftime('%Y-%m-%d')
    if today >= CERT_EXPIRES:
        print('This learning.py is expired. Please download a newer version.')
        exit(1)

check_version()
check_cert()

# start server ################################################################

import os, io, json, subprocess, tempfile, ssl
from urllib import parse
from http.server import HTTPServer, BaseHTTPRequestHandler, SimpleHTTPRequestHandler

EXEC = sys.executable
PORT = 39093
TEMP = tempfile.mkdtemp(suffix='_py', prefix='learn_python_')

HTML_INDEX = r'''
<html>
  <head><title>Learning Python</title></head>
  <body>
    <form method="post" action="/run">
      <textarea name="code" style="width:90%;height: 600px"></textarea>
      <p><button type="submit">Run</button></p>
    </form>
  </body>
</html>
'''

class LearningHTTPRequestHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        self.close_connection = True
        if self.path != '/':
            return self.send_error(404)
        self._sendHttpHeader('text/html')
        self._sendHttpBody(HTML_INDEX)

    def do_POST(self):
        self.close_connection = True
        if self.path != '/run':
            return self.send_error(400)
        print('Prepare code...')
        body = self.rfile.read(int(self.headers['Content-length']))
        qs = parse.parse_qs(body.decode('utf-8'))
        if not 'code' in qs:
            return self.send_error(400)
        code = qs['code'][0]
        r = dict()
        try:
            fpath = write_py(get_name(), code)
            print('Execute: %s %s' % (EXEC, fpath))
            r['output'] = decode(subprocess.check_output([EXEC, fpath], stderr=subprocess.STDOUT, timeout=5))
        except subprocess.CalledProcessError as e:
            r = dict(error='Exception', output=decode(e.output))
        except subprocess.TimeoutExpired as e:
            r = dict(error='Timeout', output='执行超时')
        except subprocess.CalledProcessError as e:
            r = dict(error='Error', output='执行错误')
        print('Execute done.')
        self._sendHttpHeader()
        self._sendHttpBody(r)

    def _sendHttpHeader(self, contentType='application/json'):
        origin = self.headers['Origin'] or 'https://www.liaoxuefeng.com'
        self.send_response(200)
        self.send_header('Content-Type', contentType)
        self.send_header('Access-Control-Allow-Origin', origin)
        self.send_header('Access-Control-Allow-Methods', 'GET,POST')
        self.send_header('Access-Control-Max-Age', '86400')
        self.end_headers()

    def _sendHttpBody(self, data):
        body = b''
        if isinstance(data, bytes):
            body = data
        elif isinstance(data, str):
            body = data.encode('utf-8', errors='ignore')
        else:
            body = json.dumps(data).encode('utf-8', errors='ignore')
        self.wfile.write(body)

def main():
    certfile = write_cert()
    httpd = HTTPServer(('127.0.0.1', PORT), LearningHTTPRequestHandler)
    httpd.socket = ssl.wrap_socket(httpd.socket, certfile=certfile, server_side=True)
    print('Ready for Python code on port %d...' % PORT)
    print('Press Ctrl + C to exit...')
    httpd.serve_forever()

# functions ###################################################################

INDEX = 0

def get_name():
    global INDEX
    INDEX = INDEX + 1
    return 'test_%d' % INDEX

def write_py(name, code):
    fpath = os.path.join(TEMP, '%s.py' % name)
    with open(fpath, 'w', encoding='utf-8') as f:
        f.write(code)
    print('Code wrote to: %s' % fpath)
    return fpath

def decode(s):
    try:
        return s.decode('utf-8')
    except UnicodeDecodeError:
        return s.decode('gbk')

# certificate #################################################################

def write_cert():
    fpath = os.path.join(TEMP, 'local.liaoxuefeng.com.pem')
    with open(fpath, 'w', encoding='utf-8') as f:
        f.write(CERT_DATA)
    return fpath

CERT_DATA = r'''
-----BEGIN RSA PRIVATE KEY-----
MIIEpAIBAAKCAQEArNs0nkOrt8Bq5latEhaUU9GB6cHwTcuzWaNPtIBEnREJPyp2
S2YqceCH2r6jjdoO+WUH44jteY4G1gz5qnOGrMDum7d5yZxr0XnAMzKNNvmQ5R+z
iOvHSYdk9BVBpx0V3zOW/a97zsJCA/1B+qyyQfWSy6LtbWTgoQ3LWYdQJ4AjL4jd
KcBmsGhs/K+xM8E9xssV6E4Swn6IoUVfLBQzqgRz10ST9cLxhOR7k/0QJcESeCMu
q7NMJgdR6A74/AOys0jzCugDf8RxJns0M+CJ+91krTdn1l0T2Wy4vRjQvAw6Xtdg
0mKEvbpxl8LhgcQQwEl3FkjqNqfW0EM2Eb8lHQIDAQABAoIBAD/e35p7NsA3AUkL
TfgZD8XI7FALsVeNpT/B8Hmpy7Cd0uTcM8m4foaFiK1zM8v+fvn4MuoIdncr26rM
MJSjC2haAdDYAtBUVCKa8kH4s+VUYg3HoPc+5+xrcwodsJynSqWm0mv6o6zKaso+
klql5Vgp/YvxL/n0BGx+RF1Yem2ddja7flzrbpgaqEbu78OEvBpXQniQRQ3u2ifS
Xl+Nyi4HKfxT58CThs8HHHHmuMX/570bA/C44aHZli/tHz5icnSwTHfdy8SlNZIt
7IEmV6W5aYRoozYyvWQt49EoZNzotBrenzIAESIzRypvbicJhz/hn0Vet7ZWomo+
hwSPmaECgYEA8///xiXb1vE1u0aKSebF7zdzeKZp+/EpTPYxxAy0cR8yaaN65nCs
tHqv8w+NiJ9zYTRoGK9950wgA0q7ZnRMFNZQvYnP/ahqnNoWPtShQERpKfF0tv9Q
G60GHXcUSAkO83VgGoXgY5adxy3UbBWOcIuNc23kfcDej4j+wC4weTMCgYEAtVt+
t938SgWiKALchB0mnKE8am5ueXKnxkvM7DT7BCFCmvP1RiASsWJZ9kgEhG4b0ZpN
uRXeFy9fOuSrnuzZA4cvKy9J4cmjzngqcs1qKFoo4jWbMxfwbj9lFZMwBmbmbone
2owdSUz0JCMozqmcvMbICFHlbVZCH8YdoOdLCG8CgYEAkN2HAB/uG/luC1hgNmw7
TEHB3vn+psSR3s200k8wupDpH2seRr7S6vyEhmzPfTQeDrJMs4tN1wuNXib6iGO3
4A82NLIjuNhLJAEfgAJCEqQLRAnFX/jJmQTrQoc2lWY7aDRh8J1XkgkUd/Mv0VQj
E5LnUocGR9tAyDtv9K33vZ0CgYB+WOHtgw/zGf2g1m1+9TgjQwluNMVugvxz3/dC
UJ7Yf7uBbJjiZBHh1t1KAV50TKnA2zluytdRW8WCqDEQpX2DQbkQ4v8b+HjQrVMV
bBqbRkTZY/NeIz1z8WKhJ0v8CdBcDl1d8OOuX5hvXLdfUzdJJUvS0AuAoumqbUHT
CZByrQKBgQDJGSxkQz610Nq1S4n9TL67zPV4aH9CwwzCHDslc87jSKdyEtaG1Mm1
vwImgZTyTQQz/ApEzZciWcTPpbYQLaGBRLie84OdkmWU8ENvui3Li60qb6Ukn7rm
vHqtNse0HUK1C5ianeVhC23Pdbo2XUn/RglH4PuuMulNXj/nuVqpzA==
-----END RSA PRIVATE KEY-----

-----BEGIN CERTIFICATE-----
MIIFlzCCBH+gAwIBAgIQDnY5H0NC4bAIvIdkO1PbfDANBgkqhkiG9w0BAQsFADBy
MQswCQYDVQQGEwJDTjElMCMGA1UEChMcVHJ1c3RBc2lhIFRlY2hub2xvZ2llcywg
SW5jLjEdMBsGA1UECxMURG9tYWluIFZhbGlkYXRlZCBTU0wxHTAbBgNVBAMTFFRy
dXN0QXNpYSBUTFMgUlNBIENBMB4XDTE4MDcwODAwMDAwMFoXDTE5MDcwODEyMDAw
MFowIDEeMBwGA1UEAxMVbG9jYWwubGlhb3h1ZWZlbmcuY29tMIIBIjANBgkqhkiG
9w0BAQEFAAOCAQ8AMIIBCgKCAQEArNs0nkOrt8Bq5latEhaUU9GB6cHwTcuzWaNP
tIBEnREJPyp2S2YqceCH2r6jjdoO+WUH44jteY4G1gz5qnOGrMDum7d5yZxr0XnA
MzKNNvmQ5R+ziOvHSYdk9BVBpx0V3zOW/a97zsJCA/1B+qyyQfWSy6LtbWTgoQ3L
WYdQJ4AjL4jdKcBmsGhs/K+xM8E9xssV6E4Swn6IoUVfLBQzqgRz10ST9cLxhOR7
k/0QJcESeCMuq7NMJgdR6A74/AOys0jzCugDf8RxJns0M+CJ+91krTdn1l0T2Wy4
vRjQvAw6Xtdg0mKEvbpxl8LhgcQQwEl3FkjqNqfW0EM2Eb8lHQIDAQABo4ICeTCC
AnUwHwYDVR0jBBgwFoAUf9OZ86BHDjEAVlYijrfMnt3KAYowHQYDVR0OBBYEFD0U
bMsvpjwYAld0A+0MK3wA9cynMCAGA1UdEQQZMBeCFWxvY2FsLmxpYW94dWVmZW5n
LmNvbTAOBgNVHQ8BAf8EBAMCBaAwHQYDVR0lBBYwFAYIKwYBBQUHAwEGCCsGAQUF
BwMCMEwGA1UdIARFMEMwNwYJYIZIAYb9bAECMCowKAYIKwYBBQUHAgEWHGh0dHBz
Oi8vd3d3LmRpZ2ljZXJ0LmNvbS9DUFMwCAYGZ4EMAQIBMIGBBggrBgEFBQcBAQR1
MHMwJQYIKwYBBQUHMAGGGWh0dHA6Ly9vY3NwMi5kaWdpY2VydC5jb20wSgYIKwYB
BQUHMAKGPmh0dHA6Ly9jYWNlcnRzLmRpZ2l0YWxjZXJ0dmFsaWRhdGlvbi5jb20v
VHJ1c3RBc2lhVExTUlNBQ0EuY3J0MAkGA1UdEwQCMAAwggEDBgorBgEEAdZ5AgQC
BIH0BIHxAO8AdQC72d+8H4pxtZOUI5eqkntHOFeVCqtS6BqQlmQ2jh7RhQAAAWR4
Q3wGAAAEAwBGMEQCICpbOL7rKNzMYP8a+HwjVFhQKROAnlQ3Ig2l5RCJz4zMAiA1
Lgzf7TUfpvEyU/yqsHNDfzuTrtVA56pPJa4xa9/Q6gB2AId1v+dZfPiMQ5lfvfNu
/1aNR1Y2/0q1YMG06v9eoIMPAAABZHhDe8YAAAQDAEcwRQIgYuPTsE8JwnVMmN0Q
Feq4u5tyO5/nMoGstlouXLwbvbECIQC9zVOzfr+7SmWEES1NMRel++nZhFFQ0pmT
LjhCQPBd2jANBgkqhkiG9w0BAQsFAAOCAQEAIkbLq1OsPZlkBmVNvFWQ6lD9SMc2
+tuaqPHF2rECQfL8EprUF9KZLP1ye2dUvZodbbB1JcgBPNcz3NX5yTi3CIiNcf/B
qPk5o726hS2Vdyk3rhkNiezNI03UHohHkQ2U4PK4iOSZUgXABjlqyuq6KgoQ00JM
LZXvOnpMPjK3jeiZK46TvPP4FlOfnyx5C1gJBUzbIEMGb9f2jwGklRKyrREJ9Dqq
9C/8q7mEL2+q8COLrX6QQb268+FRm5l0YpRwVF+ciq2jsUO3UX3cJf5SRjq3gvcn
cRROlQJP6aKj8AWyU44RStiJzqzPkFbVQGhrmZ9dtiupZLeNZQLlWAVYlA==
-----END CERTIFICATE-----

-----BEGIN CERTIFICATE-----
MIIErjCCA5agAwIBAgIQBYAmfwbylVM0jhwYWl7uLjANBgkqhkiG9w0BAQsFADBh
MQswCQYDVQQGEwJVUzEVMBMGA1UEChMMRGlnaUNlcnQgSW5jMRkwFwYDVQQLExB3
d3cuZGlnaWNlcnQuY29tMSAwHgYDVQQDExdEaWdpQ2VydCBHbG9iYWwgUm9vdCBD
QTAeFw0xNzEyMDgxMjI4MjZaFw0yNzEyMDgxMjI4MjZaMHIxCzAJBgNVBAYTAkNO
MSUwIwYDVQQKExxUcnVzdEFzaWEgVGVjaG5vbG9naWVzLCBJbmMuMR0wGwYDVQQL
ExREb21haW4gVmFsaWRhdGVkIFNTTDEdMBsGA1UEAxMUVHJ1c3RBc2lhIFRMUyBS
U0EgQ0EwggEiMA0GCSqGSIb3DQEBAQUAA4IBDwAwggEKAoIBAQCgWa9X+ph+wAm8
Yh1Fk1MjKbQ5QwBOOKVaZR/OfCh+F6f93u7vZHGcUU/lvVGgUQnbzJhR1UV2epJa
e+m7cxnXIKdD0/VS9btAgwJszGFvwoqXeaCqFoP71wPmXjjUwLT70+qvX4hdyYfO
JcjeTz5QKtg8zQwxaK9x4JT9CoOmoVdVhEBAiD3DwR5fFgOHDwwGxdJWVBvktnoA
zjdTLXDdbSVC5jZ0u8oq9BiTDv7jAlsB5F8aZgvSZDOQeFrwaOTbKWSEInEhnchK
ZTD1dz6aBlk1xGEI5PZWAnVAba/ofH33ktymaTDsE6xRDnW97pDkimCRak6CEbfe
3dXw6OV5AgMBAAGjggFPMIIBSzAdBgNVHQ4EFgQUf9OZ86BHDjEAVlYijrfMnt3K
AYowHwYDVR0jBBgwFoAUA95QNVbRTLtm8KPiGxvDl7I90VUwDgYDVR0PAQH/BAQD
AgGGMB0GA1UdJQQWMBQGCCsGAQUFBwMBBggrBgEFBQcDAjASBgNVHRMBAf8ECDAG
AQH/AgEAMDQGCCsGAQUFBwEBBCgwJjAkBggrBgEFBQcwAYYYaHR0cDovL29jc3Au
ZGlnaWNlcnQuY29tMEIGA1UdHwQ7MDkwN6A1oDOGMWh0dHA6Ly9jcmwzLmRpZ2lj
ZXJ0LmNvbS9EaWdpQ2VydEdsb2JhbFJvb3RDQS5jcmwwTAYDVR0gBEUwQzA3Bglg
hkgBhv1sAQIwKjAoBggrBgEFBQcCARYcaHR0cHM6Ly93d3cuZGlnaWNlcnQuY29t
L0NQUzAIBgZngQwBAgEwDQYJKoZIhvcNAQELBQADggEBAK3dVOj5dlv4MzK2i233
lDYvyJ3slFY2X2HKTYGte8nbK6i5/fsDImMYihAkp6VaNY/en8WZ5qcrQPVLuJrJ
DSXT04NnMeZOQDUoj/NHAmdfCBB/h1bZ5OGK6Sf1h5Yx/5wR4f3TUoPgGlnU7EuP
ISLNdMRiDrXntcImDAiRvkh5GJuH4YCVE6XEntqaNIgGkRwxKSgnU3Id3iuFbW9F
UQ9Qqtb1GX91AJ7i4153TikGgYCdwYkBURD8gSVe8OAco6IfZOYt/TEwii1Ivi1C
qnuUlWpsF1LdQNIdfbW3TSe0BhQa7ifbVIfvPWHYOu3rkg1ZeMo6XRU9B4n5VyJY
RmE=
-----END CERTIFICATE-----
'''

# start main at last ##########################################################

if __name__ == '__main__':
    main()
