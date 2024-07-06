import os
import json
import pathlib
import pytest
import subprocess
import urllib.request
import urllib.error

@pytest.fixture
def my_ip():
    if not pathlib.Path('my_ip.txt').is_file():
        f = open('my_ip.txt','w')
        f.write(os.popen('curl ident.me').read())
        f.close()

    return open('my_ip.txt').read()

def test_apache_static(my_ip):
    err = None
    try:
        res = urllib.request.urlopen(f'http://{my_ip}')
        assert len(res.read()) > 0
    except urllib.error.HTTPError as e:
        err = e
    except urllib.error.URLError as e:
        err = e
    except Exception as e:
        err = e

    if err:
        assert False, f"An error occurred: {err}"

@pytest.fixture
def get_cgi(my_ip):
    err = None
    try:
        res = urllib.request.urlopen(f'http://{my_ip}/cgi-bin/test.sh')
        return res
    except urllib.error.HTTPError as e:
        err = e
    except urllib.error.URLError as e:
        err = e
    except Exception as e:
        err = e

    if err:
        assert False, f"An error occurred: {err}"

    
def test_apache_dynamic_header(get_cgi):
    assert get_cgi.headers.get_content_type() == 'text/plain'

def test_apache_dynamic_content(get_cgi):
    assert len(get_cgi.read().decode('utf-8')) > 0
    
def test_dns(my_ip):
    d = json.loads(urllib.request.urlopen('http://api.wmdd4950.com/arecord/list').read())
    assert my_ip in d.values(), f'{my_ip} DNS has not been setup'
