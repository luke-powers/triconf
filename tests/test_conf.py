'''Run with pytest.

'''

import os
import pytest
import triconf

fake_conf = 'fake_conf.ini'

def fake_conf_setup(file_contents=None):
    open(fake_conf, 'w').write(file_contents)

def fake_conf_tear_down():
    os.unlink(fake_conf)

def test_conf_ini_loaded_into_namespace():
    fake_conf_setup("test_param='loaded'")
    resp = triconf.initialize('bob', conf_file_names='fake_conf.ini')
    assert hasattr(resp, 'test_param')
    assert resp.test_param == 'loaded'
    fake_conf_tear_down()

def test_conf_raise_exception_bad_conf_file():
    pytest.raises(triconf.ConfException, triconf.initialize, 'bob', conf_file_names='none.ini')

def test_conf_update_namespace():
    fake_conf_setup("arg_test='loaded'") # Should not have 'loaded' in output
    resp = triconf.initialize('bob', conf_file_names='fake_conf.ini')
    resp.arg_test = 'not_absorbed'
    class Test(object):
        arg_test = 'absorbed_correctly'
        __dont_gather__ = 'Gathered'
    resp(Test.__dict__)
    assert resp.arg_test == 'absorbed_correctly'
    assert not hasattr(resp, '__dont_gather__')
    fake_conf_tear_down()
