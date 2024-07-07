import os
import stat
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


def test_cgi_script_setup():
    with open('/usr/lib/cgi-bin/test.sh') as test_sh:
        content = test_sh.read()
        assert '#!/bin/bash' in content

def test_cgi_script_permission():

    file_stat = os.stat('/usr/lib/cgi-bin/test.sh')

    # Owner permissions
    owner_read = bool(file_stat.st_mode & stat.S_IRUSR)
    owner_write = bool(file_stat.st_mode & stat.S_IWUSR)
    owner_execute = bool(file_stat.st_mode & stat.S_IXUSR)
    
    # Group permissions
    group_read = bool(file_stat.st_mode & stat.S_IRGRP)
    group_write = bool(file_stat.st_mode & stat.S_IWGRP)
    group_execute = bool(file_stat.st_mode & stat.S_IXGRP)
    
    # Others permissions
    others_read = bool(file_stat.st_mode & stat.S_IROTH)
    others_write = bool(file_stat.st_mode & stat.S_IWOTH)
    others_execute = bool(file_stat.st_mode & stat.S_IXOTH)

    assert owner_read and owner_write and owner_execute
    assert group_read and not group_write and group_execute
    assert others_read and not others_write and others_execute
    

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
