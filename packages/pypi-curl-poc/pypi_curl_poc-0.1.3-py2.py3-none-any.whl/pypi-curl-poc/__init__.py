#!/usr/bin/env python3.11
# -*- coding: utf-8 -*-

import requests


def curl_get(url, params=None):
    """Mimic the curl -G command."""
    response = requests.get(url, params=params)
    return response.text
