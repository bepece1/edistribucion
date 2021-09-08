#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# This example aims at testing the backend with no integration. Thanks a lot trocotronic for this backend
"""
Created on Wed May 20 11:51:36 2020

@author: trocotronic
"""
USER = ''
PASSWORD = ''
CUPS = ''

from backend.EdistribucionAPI import Edistribucion



edis = Edistribucion(USER,PASSWORD)
edis.login()
r = edis.get_cups()
print(r)

if CUPS:
    for c in r['data']['lstCups']:
        if c['Name'] == CUPS:
            cups_id = c['Id']
else:
    cups_id = r['data']['lstCups'][0]['Id']
print('Cups id: ',cups_id)
meter = edis.get_meter(cups_id)
print('Meter: ',meter)
