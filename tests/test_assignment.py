import os
import stat
import pathlib
import pytest


@pytest.fixture(scope="session")
def my_ip():
    if not pathlib.Path('my_ip.txt').is_file():
        f = open('my_ip.txt','w')
        f.write(os.popen('curl ident.me').read())
        f.close()

    return open('my_ip.txt').read()

@pytest.fixture(scope="session")
def content_test_sh():
    if not pathlib.Path('test.sh').is_file():
        os.popen('cp /usr/lib/cgi-bin/test.sh .').read()

    try:
        return open('test.sh').read()
    except:
        return None

@pytest.fixture(scope="session")
def curl_localhost():
    output_file = 'curl_localhost.txt'
    if not pathlib.Path(output_file).is_file():
        os.popen(f'curl localhost > {output_file}').read()
    return open(output_file).read()

@pytest.fixture(scope="session")
def curl_test_sh():
    output_file = 'curl_test_sh.txt'
    if not pathlib.Path(output_file).is_file():
        os.popen(f'curl localhost/cgi-bin/test.sh > {output_file}').read()
    return open(output_file).read()

def test_cgi_script_permission(content_test_sh):

    file_stat = os.stat('test.sh')

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
    
def test_curl_localhost(curl_localhost):
    assert len(curl_localhost) > 0
    
def test_content_test_sh(content_test_sh):
    assert content_test_sh != None

def test_test_sh(curl_test_sh):
    assert len(curl_test_sh) > 0

def test_test_sh_header(curl_test_sh):
    assert 'text/plain' in curl_test_sh

def test_dns(my_ip):
    d = json.loads(urllib.request.urlopen('http://api.wmdd4950.com/arecord/list').read())
    assert my_ip in d.values(), f'{my_ip} DNS has not been setup'
