#!/usr/bin/env python3
# -*- coding: utf-8 -*-

r'''
learning.py

A Python 3 tutorial from https://www.liaoxuefeng.com

Usage:

$ python3 learning.py
'''

# check #######################################################################

import sys
from datetime import datetime

CERT_EXPIRES = '2020-08-07'

def check_version():
    v = sys.version_info
    if v.major == 3 and v.minor >= 6:
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
MIIEpAIBAAKCAQEArUtX5vRI7RsCBEN8sIPskQyLJhsXzxQ947dcH2so0uuCYodm
wkuKwMtjCvP5nnM2PRaJMSD3ke4OA2BdD+CWGFmoXdD8yJbAOh6da4boOi2Rh174
YlZLcpGBhbqprXlRC1Ip0jzW38y4dOW9m9L1QEALoHZ6vJG1sYouLEfPLubI9+bg
VO1WipHBebuT4OosivsJxBhNqe1dR7rCkCjV1v/iBmbJCujrH9rri12LmksL0HhW
7V5mccae07mao0tfu1esFeLqYWM7+heQ82qXwg1WfbztXWJkP088fPjFGWSAVcZS
9RzPEt/lC34If15AqSEr60zKDkQ1olU36YHO+wIDAQABAoIBAAGuaJ4VLPyelaCX
S7HmDcOt1KRxgIPMpU8SG9gy23S0aTxDJl7oibeWIZIHzO+vHCMalrPTJzkTZK++
sxhw1t6fRrq7nirktN0Q0qPU7WgxwfwyEoSDDtH/5xBLlSgu3veWUVE4sDhVTaLW
Cca7FLsOBAQyB2h7R2vUtImkcWD57c4kDH90hN8htl+KFhMrBctiRbzvcB2tk/xO
e46YJ1GSRQg3OQQGQJeDczAoGzsv20pYuvDmqlhrQC64Zxxz7nZfftbCztvuVoPj
RGLRm/wRXPjujqBXivePanxYLP4dUOa6/NK7J5uea41e3CHIPTk1id4G15Knkypv
vQcJ2/kCgYEA3LAwxc/+DR3uwbcM5ZWeFK+16LfR+fF/ZNtm2vHuN458ZpcbBELO
rhUmye30LE0wwSPgPtjkXQ2r2BZD9fzji2jIGaWtsSvigjhMGRWOhVtlfB5kBNx+
Kk3PjunOId+HodVvOQxxXWbljiLQCNG3di7r+7ojcsj+ruos7iBSZ5kCgYEAyQXO
rLx9WP+xoCu3OV1PD5LFcvb/x9R3xMzEsZGYh/s969bNHkPvT/4BFcMBVv8X0WdE
kY04YJd3m1XzmOXeTR7XSZhG0sekYRbnEl8aWyMTmuhtjXwPHYReTx9ZEl3oRTfY
lubd51QPnArwGD+E9+1i2uCNjbFiDOv/+Tedt7MCgYEAjfLeTD5OoM1CB2PgbcPg
3Flw3nFuJCCL2qms7ON0YFPL/IjxHbqDCkIcowHlbqFv3Ktgz8veh2QFxoX7zLuO
+Nq66pRAtpcNqMjhWbkd5PU2v7EkkGPq2vcVrE0DA5KtwRBx6/Xu7S8ENHp76VBL
ez8PFulRZ8GU35lMsRYlKvECgYEAl1tRBwyREK7NTj08IuwXuDEZi/tgEVTvrPVE
8DIg99n7AJTmMnCSQteMd5cxbhB6HYg0v6bmGQxS2Vm5JZmGbOjYzqfiQ5hgM14s
M8/5pz9c5pk0y3/qXZ4p6EdBKKweU+e9o7lGwYOwkRxHNOq2snpBoW3MBzDVE8eq
Hzp5/TMCgYAomXNpRtHcXt2VhJR0FefYOfj4n4cGAtg8/dNlJSzkhR6ad2KniCz1
KgedQRAsqRSh0UZgTTxPA5Y/zpAvmAHFB7fr9syWb1QSBBvgLWkzpUgaEEJBRjwu
s2urAziMIcPf+mZf9rFscD/JKYQo3fHSd/UWTSM0SkQNu7uHqcgN8g==
-----END RSA PRIVATE KEY-----
-----BEGIN CERTIFICATE-----
MIIFkjCCBHqgAwIBAgIQAt7xtFqJsgRZGvKRMyO9njANBgkqhkiG9w0BAQsFADBy
MQswCQYDVQQGEwJDTjElMCMGA1UEChMcVHJ1c3RBc2lhIFRlY2hub2xvZ2llcywg
SW5jLjEdMBsGA1UECxMURG9tYWluIFZhbGlkYXRlZCBTU0wxHTAbBgNVBAMTFFRy
dXN0QXNpYSBUTFMgUlNBIENBMB4XDTE5MDYwOTAwMDAwMFoXDTIwMDgwNzEyMDAw
MFowIDEeMBwGA1UEAxMVbG9jYWwubGlhb3h1ZWZlbmcuY29tMIIBIjANBgkqhkiG
9w0BAQEFAAOCAQ8AMIIBCgKCAQEArUtX5vRI7RsCBEN8sIPskQyLJhsXzxQ947dc
H2so0uuCYodmwkuKwMtjCvP5nnM2PRaJMSD3ke4OA2BdD+CWGFmoXdD8yJbAOh6d
a4boOi2Rh174YlZLcpGBhbqprXlRC1Ip0jzW38y4dOW9m9L1QEALoHZ6vJG1sYou
LEfPLubI9+bgVO1WipHBebuT4OosivsJxBhNqe1dR7rCkCjV1v/iBmbJCujrH9rr
i12LmksL0HhW7V5mccae07mao0tfu1esFeLqYWM7+heQ82qXwg1WfbztXWJkP088
fPjFGWSAVcZS9RzPEt/lC34If15AqSEr60zKDkQ1olU36YHO+wIDAQABo4ICdDCC
AnAwHwYDVR0jBBgwFoAUf9OZ86BHDjEAVlYijrfMnt3KAYowHQYDVR0OBBYEFOe3
Dec5wHbk5Hf8h6l2DDHgHxHhMCAGA1UdEQQZMBeCFWxvY2FsLmxpYW94dWVmZW5n
LmNvbTAOBgNVHQ8BAf8EBAMCBaAwHQYDVR0lBBYwFAYIKwYBBQUHAwEGCCsGAQUF
BwMCMEwGA1UdIARFMEMwNwYJYIZIAYb9bAECMCowKAYIKwYBBQUHAgEWHGh0dHBz
Oi8vd3d3LmRpZ2ljZXJ0LmNvbS9DUFMwCAYGZ4EMAQIBMH0GCCsGAQUFBwEBBHEw
bzAhBggrBgEFBQcwAYYVaHR0cDovL29jc3AuZGNvY3NwLmNuMEoGCCsGAQUFBzAC
hj5odHRwOi8vY2FjZXJ0cy5kaWdpdGFsY2VydHZhbGlkYXRpb24uY29tL1RydXN0
QXNpYVRMU1JTQUNBLmNydDAJBgNVHRMEAjAAMIIBAwYKKwYBBAHWeQIEAgSB9ASB
8QDvAHUApLkJkLQYWBSHuxOizGdwCjw1mAT5G9+443fNDsgN3BAAAAFrOiI+ygAA
BAMARjBEAiAGlx0z2YTgQMyVva5eRZTnry0rUjPGCXWP1Y4/XgpO9wIgSBtIfCjH
GC+xLuvUOEQZAfnh6xoDFJ6urTk/tdkJ/BYAdgCHdb/nWXz4jEOZX73zbv9WjUdW
Nv9KtWDBtOr/XqCDDwAAAWs6Ij+WAAAEAwBHMEUCIQDNqJG+8r5IwXDOLHyfUkg8
XpkaMYjncE5mSMLwyprt1gIgLAilaTtP0zlar11n3LTVhz/XG8o5kUoFIgps/cDS
PN0wDQYJKoZIhvcNAQELBQADggEBAEPFPqZE03u06PZ9jMpoke4CXHF3iTBABuTA
//g6w7Pn/DlMuHs5OS2S4RXQs5QJfdLpS7TsYatYmfhDO+b13QuBM/09BFh+KXsJ
ITbS9omy8eB/IK+OGCIJwoj1psoU4tw/MO2sly5N8rgJgYytD1U0+BbDIhWY1jlK
lP3rTkV1OkoGfPFzjjqk5VIiNdGXqn/aeXMbycbyyyDGwhLmqMARWLiDvQLywwzu
cGxJS4s+oP4SIYVH+sfyG51fRSTIyqzI8tP1MNuPi1R6r88NijyQ+f/tQs8R3OB+
AHcthgqp6TI5qsN89vJzqD4NTBBrCcyU1PshW5rAjJelnJlmfIU=
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
