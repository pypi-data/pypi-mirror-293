import requests_odigos


def test_can_access_urllib3_attribute():
    requests_odigos.packages.urllib3


def test_can_access_idna_attribute():
    requests_odigos.packages.idna


def test_can_access_chardet_attribute():
    requests_odigos.packages.chardet
