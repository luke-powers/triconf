'''Run with pytest.

'''

import os
import pytest
import triconf

FAKE_CONF = 'fake_conf.ini'
NON_EXISTANT_FILENAME = 'nonexistant.ini'


def fake_conf_setup(file_contents=None):
    open(FAKE_CONF, 'w').write(file_contents)


def fake_conf_tear_down():
    os.unlink(FAKE_CONF)


def test_conf_ini_loaded_into_namespace():
    fake_conf_setup("test_param='loaded'")
    resp = triconf.initialize('bob', conf_file_names='fake_conf.ini')
    assert hasattr(resp, 'test_param')
    assert resp.test_param == 'loaded'
    fake_conf_tear_down()


def test_conf_update_namespace():
    fake_conf_setup("arg_test='loaded'")  # Should not have 'loaded' in output
    resp = triconf.initialize('bob', conf_file_names='fake_conf.ini')
    resp.arg_test = 'not_absorbed'

    class Test(object):
        arg_test = 'absorbed_correctly'
        __dont_gather__ = 'Gathered'
    resp(Test.__dict__)
    assert resp.arg_test == 'absorbed_correctly'
    assert not hasattr(resp, '__dont_gather__')
    fake_conf_tear_down()


def test_specified_missing_conf_file():
    # Assert that a nonexistant ini is created.
    triconf.initialize('bob', conf_file_names=NON_EXISTANT_FILENAME)
    assert os.path.exists(NON_EXISTANT_FILENAME)
    os.unlink(NON_EXISTANT_FILENAME)


def test_no_conf_file():
    # Assert that a nonexistant ini is created.
    triconf.initialize('bob')

