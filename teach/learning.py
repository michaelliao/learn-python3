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

CERT_EXPIRES = '2018-07-01'

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
MIIEpAIBAAKCAQEA5b3zv77bzN8JShoXkVjXFG9NK342wnfgye+NmuSoRfCMPrwL
GToJZiwxokXGyVY8obmQA69WUgonpuotp0AhDK8bOvykKuX+7MyE36sh9TUVOiIw
6D3ODG2E1K5IIEytfGhuPmeJe3OapnL/lJytlLhonu63VEf+jpYh6I/gXD4hZu1N
tx4rOeJLl3qSFgRgX4oBZtO0d4aHop/XW5XcdaeuJxIW5qw7PxXqlch4h9TUs0Og
udko380DrO9pmTuVXr2rtk6Jy96wDAVwsAiSX85FF59Q3QmjDzM+fx8a/vyWkxOw
9dT0DzfZBJ9g/tPk13ir14U1vPpDMO1lIXjKZQIDAQABAoIBAEp+FwT7W8XII/j1
EOM+DS9BD6KkoBjaSfbwR9gLgEx9PNwymN6rJNUOS2G0gkpSPgKqannnZnPfew/y
Kq9qacz1Ej1EIe8O+GPLxOHJWY9qkOFyqK0FLUR2VnWntRdUBYSrT+PIKpnu2BxU
eW60hswMJ1AxUxxu46lUINaJoFQH7ANHzpCxXFiWDiVK8VCCFS3MaJfqz945zLdg
orHMty+gCcaWRX9wanZ5k9RmX2qzqLAAhlnKIfmItpel8HTppOk1taVDopUgPGd+
8IG7IANbRlykkeBvlA5soSk7RNM2+crHcdCz5ehoSjMHsY3e99EPoPjKQmb3Ak0p
zgtjPpkCgYEA8p+eULq0OM2anLQeOqQe2QNxkTuriOI2qyobOnCYAJRFlxCLJ8K8
OIf+srIJUYzJsGmPSqo8iizM5V9bmBRihYnPwePUJS0af8G2vdeJARoAFBo4LZNi
YBN3Gi6hKo8hDgOPQ6D2a25NXYua4z5HlOb8PU6JhX1/6O6yv4ScZh8CgYEA8miG
QxHbx3a7Zfy3/QCQrEwmbp9k49ex/DZvh50N5MqG9h6lb6+ct+qUT7HkvcXUrBxL
6HP7aLVUTTvo9z10sBh1Kt1UQP/57JbKQNMCYKUbMxZH59XdFPzVwkbyDE7Z29tf
8QEMnk9CM6HbvbQDSvOZ04IsfSEstMEPKqVmFvsCgYEAsOSborRdTcTp4zKXj521
N/gAxyjAKe70eNscOwF4cYOpMTjInFaosHbGxjZ0ANcq/coYxRFVTlDXmqxptXm3
UzFlHjIjrG80EM2FlOgeZYU1ZXKwXtpEMVQ/1AEHVGZCbVs/CsnCoBUtpvRwGxp/
ShsW8QPf1EnqBkRyYpwnA3UCgYA5nrLbWnFddlGRKoMpdmrtKaSxAt5ecjTyeJYG
LETTL3jpI9u7MokUBoR+dRCkM1QcHRXGCVunRgLl4Om9azRDb2zaZYXTdYUYwbcN
tZqJEnXmrNMmvmUwyfCdn3OFjXCnm/uwM8mmD7zyvPSYoSNvO3xDFFwy2iHgTUun
nW0o5QKBgQCF/mCu/z1+CsddcHu1RYjnG08uVk0ErjTLB5Qy0YI2NWVE2zdV9fi9
MWn7S+oEcmjaMdXdF0W/MDyB8TLUSdsXGHPl/vRizK3vhDQGxQ+y3ru8GEVq8BjX
YePMDifbgHDXrCeBeb7TypefD/ScxdVJdI9sPSno20AehzDkXcAssQ==
-----END RSA PRIVATE KEY-----

-----BEGIN CERTIFICATE-----
MIIFzTCCBLWgAwIBAgIQB594sjWBo6qup5zlKa2F7zANBgkqhkiG9w0BAQsFADCB
lzELMAkGA1UEBhMCQ04xJTAjBgNVBAoTHFRydXN0QXNpYSBUZWNobm9sb2dpZXMs
IEluYy4xHzAdBgNVBAsTFlN5bWFudGVjIFRydXN0IE5ldHdvcmsxHTAbBgNVBAsT
FERvbWFpbiBWYWxpZGF0ZWQgU1NMMSEwHwYDVQQDExhUcnVzdEFzaWEgRFYgU1NM
IENBIC0gRzUwHhcNMTcwNzA1MDAwMDAwWhcNMTgwNzA1MjM1OTU5WjAgMR4wHAYD
VQQDDBVsb2NhbC5saWFveHVlZmVuZy5jb20wggEiMA0GCSqGSIb3DQEBAQUAA4IB
DwAwggEKAoIBAQDlvfO/vtvM3wlKGheRWNcUb00rfjbCd+DJ742a5KhF8Iw+vAsZ
OglmLDGiRcbJVjyhuZADr1ZSCiem6i2nQCEMrxs6/KQq5f7szITfqyH1NRU6IjDo
Pc4MbYTUrkggTK18aG4+Z4l7c5qmcv+UnK2UuGie7rdUR/6OliHoj+BcPiFm7U23
His54kuXepIWBGBfigFm07R3hoein9dbldx1p64nEhbmrDs/FeqVyHiH1NSzQ6C5
2SjfzQOs72mZO5Vevau2TonL3rAMBXCwCJJfzkUXn1DdCaMPMz5/Hxr+/JaTE7D1
1PQPN9kEn2D+0+TXeKvXhTW8+kMw7WUheMplAgMBAAGjggKJMIIChTAgBgNVHREE
GTAXghVsb2NhbC5saWFveHVlZmVuZy5jb20wCQYDVR0TBAIwADBhBgNVHSAEWjBY
MFYGBmeBDAECATBMMCMGCCsGAQUFBwIBFhdodHRwczovL2Quc3ltY2IuY29tL2Nw
czAlBggrBgEFBQcCAjAZDBdodHRwczovL2Quc3ltY2IuY29tL3JwYTAfBgNVHSME
GDAWgBRtWMd/GufhPy6mjJc1Qrv00zisPzAOBgNVHQ8BAf8EBAMCBaAwHQYDVR0l
BBYwFAYIKwYBBQUHAwEGCCsGAQUFBwMCMIGbBggrBgEFBQcBAQSBjjCBizA8Bggr
BgEFBQcwAYYwaHR0cDovL3RydXN0YXNpYTItb2NzcC5kaWdpdGFsY2VydHZhbGlk
YXRpb24uY29tMEsGCCsGAQUFBzAChj9odHRwOi8vdHJ1c3Rhc2lhMi1haWEuZGln
aXRhbGNlcnR2YWxpZGF0aW9uLmNvbS90cnVzdGFzaWFnNS5jcnQwggEDBgorBgEE
AdZ5AgQCBIH0BIHxAO8AdQDd6x0reg1PpiCLga2BaHB+Lo6dAdVciI09EcTNtuy+
zAAAAV0QuhtTAAAEAwBGMEQCIERpJLcXX4eFEW02eZMh6EYFW236foQrCsakOgQQ
NW96AiBCE6/7vrUxWKf964i4D9z2NA0TCuXm9giVgQaFju0XXQB2AKS5CZC0GFgU
h7sTosxncAo8NZgE+RvfuON3zQ7IDdwQAAABXRC6G5MAAAQDAEcwRQIhAK4GeiTU
OQcjGFvLAugOMIEKCEuiJsEu0t+f1ql5Edn2AiAUqqLMw87IkjMnJsbEUGsHkng0
KL6MLDC3BaHVcH6HsjANBgkqhkiG9w0BAQsFAAOCAQEAYDU2DSBh/63brAW/VWlQ
PQIZzWhji6209MG5hg/RN3Zo9uoz2GodNWwOSkvcFVUz9oBExLfcfhZAsBz26dgs
abWstAje63oduhXU9MR1LDFfG6GLit0Pou0yiS0hfg3jpxpYCIo97QAe8bkuMdRQ
7V09yKKo44M+iXbkIUivnM1ckYJHU9xQ3y8/q/DQajUmVIEPRzmyz6B3tP4WA11T
X5T89OK6osvLcYSJXvxOeR3J8Ohxdwi+PRX4BCgXgTseOj+biwJuCo9z7uwvCoXG
fdilj1tXNa5eDtSRplqbFB+kPGkP/NZ5b1+huarDqE/aeNpmREqONhxi49KB1/9u
1w==
-----END CERTIFICATE-----

-----BEGIN CERTIFICATE-----
MIIFZTCCBE2gAwIBAgIQOhAOfxCeGsWcxf/2QNXkQjANBgkqhkiG9w0BAQsFADCB
yjELMAkGA1UEBhMCVVMxFzAVBgNVBAoTDlZlcmlTaWduLCBJbmMuMR8wHQYDVQQL
ExZWZXJpU2lnbiBUcnVzdCBOZXR3b3JrMTowOAYDVQQLEzEoYykgMjAwNiBWZXJp
U2lnbiwgSW5jLiAtIEZvciBhdXRob3JpemVkIHVzZSBvbmx5MUUwQwYDVQQDEzxW
ZXJpU2lnbiBDbGFzcyAzIFB1YmxpYyBQcmltYXJ5IENlcnRpZmljYXRpb24gQXV0
aG9yaXR5IC0gRzUwHhcNMTYwODExMDAwMDAwWhcNMjYwODEwMjM1OTU5WjCBlzEL
MAkGA1UEBhMCQ04xJTAjBgNVBAoTHFRydXN0QXNpYSBUZWNobm9sb2dpZXMsIElu
Yy4xHzAdBgNVBAsTFlN5bWFudGVjIFRydXN0IE5ldHdvcmsxHTAbBgNVBAsTFERv
bWFpbiBWYWxpZGF0ZWQgU1NMMSEwHwYDVQQDExhUcnVzdEFzaWEgRFYgU1NMIENB
IC0gRzUwggEiMA0GCSqGSIb3DQEBAQUAA4IBDwAwggEKAoIBAQC39aSJZG/97x3a
6Qmuc9+MubagegRAVUmFYHTYTs8IKB2pM7wXN7W8mekdZaEgUjDFxvRBK/DhTb7U
8ONLsKKdT86aOhzbz2noCTn9wPWnGwkg+/4YKg/dPQQdV9tMsSu0cwqInWHxSAkm
AI1hYFC9D7Sf7Hp/5cRcD+dK454YMRzNOGLQnCVI8JEqrz6o9SOvQNTqTcfqt6DC
0UlXG+MPD1eNPjlzf1Vwaab+VSTgySoC+Ikbq2VsdykeOiGXW/OIiASH7+2LcR05
PmQ7GEOlM8yzoVojFpM8sHz+WxI05ZOPri5+vX3HhHHjWr5432G0dVmgohnZvlVZ
oy8XrlbpAgMBAAGjggF2MIIBcjASBgNVHRMBAf8ECDAGAQH/AgEAMC8GA1UdHwQo
MCYwJKAioCCGHmh0dHA6Ly9zLnN5bWNiLmNvbS9wY2EzLWc1LmNybDAOBgNVHQ8B
Af8EBAMCAQYwLgYIKwYBBQUHAQEEIjAgMB4GCCsGAQUFBzABhhJodHRwOi8vcy5z
eW1jZC5jb20wYQYDVR0gBFowWDBWBgZngQwBAgEwTDAjBggrBgEFBQcCARYXaHR0
cHM6Ly9kLnN5bWNiLmNvbS9jcHMwJQYIKwYBBQUHAgIwGRoXaHR0cHM6Ly9kLnN5
bWNiLmNvbS9ycGEwHQYDVR0lBBYwFAYIKwYBBQUHAwEGCCsGAQUFBwMCMCkGA1Ud
EQQiMCCkHjAcMRowGAYDVQQDExFTeW1hbnRlY1BLSS0yLTYwMTAdBgNVHQ4EFgQU
bVjHfxrn4T8upoyXNUK79NM4rD8wHwYDVR0jBBgwFoAUf9Nlp8Ld7LvwMAnzQzn6
Aq8zMTMwDQYJKoZIhvcNAQELBQADggEBABUphhBbeG7scE3EveIN0dOjXPgwgQi8
I2ZAKYm6DawoGz1lEJVdvFmkyMbP973X80b7mKmn0nNbe1kjA4M0O0hHaMM1ZaEv
7e9vHEAoGyysMO6HzPWYMkyNxcCV7Nos2Uv4RvLDpQHh7P4Kt6fUU13ipcynrtQD
1lFUM0yoTzwwFsPu3Pk+94hL58ErqwqJQwxoHMgLIQeMVHeNKcWFy1bddSbIbCWU
Zs6cMxhrra062ZCpDCbxyEaFNGAtYQMqNz55Z/14XgSUONZ/cJTns6QKhpcgTOwB
fnNzRnk+aWreP7osKhXlz4zs+llP7goBDKFOMMtoEXx3YjJCKgpqmBU=
-----END CERTIFICATE-----
'''

# start main at last ##########################################################

if __name__ == '__main__':
    main()
