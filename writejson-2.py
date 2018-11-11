#!/usr/bin/python
# Filename: writejson-2.py
# Author: Zixiang Nie (znie@ufl.edu)
# Modified Nov 11 2018

import sys
import collections
import http.client
import csv
import json
import time
from time import sleep

chNum = sys.argv[1]
filename = sys.argv[2]


def csv2json(filename, key):
    csvfile = open(filename, 'r')
    fieldnames = ('field1', 'field2', 'field3', 'field4')
    reader = csv.DictReader(csvfile, fieldnames)
    data = collections.OrderedDict()
    data['write_api_key'] = key
    subdata = []
    macSet = set()
    for row in reader:
        if row['field2'] == '' or row['field2'] == '00:00:00:00:00:00' or row['field3'] == '0':
            continue
        temp = collections.OrderedDict()
        temp['delta_t'] = '1'
        temp['field1'] = row['field1']
        temp['field2'] = row['field2']
        macSet.add(row['field2'])
        temp['field3'] = row['field3']
        temp['field4'] = row['field4']
        subdata.append(temp)

    # print(subdata[50])

    # for i in range(len(subdata)-1, -1, -1):
    #     print(subdata[i])

    for mac in macSet:
        for i in range(len(subdata) - 1, -1, -1):
            if subdata[i]['field2'] == mac:
                lastTime = subdata[i]['field1']
                break
        for i in range(len(subdata) - 1, -1, -1):
            if subdata[i]['field2'] == mac:
                if float(subdata[i]['field1']) >= float(lastTime):
                    lastTime = subdata[i]['field1']
                    continue
                else:
                    if (float(lastTime) - float(subdata[i]['field1'])) < 1:
                        del subdata[i]
                    else:
                        lastTime = subdata[i]['field1']

    data['updates'] = subdata
    # print(data)
    output = json.dumps(data, indent=4, separators=(',', ':'))
    # print(output)
    index = filename.find('.')
    jsonfile = open(filename[:index] + '.json', 'w')
    jsonfile.write(output)
    jsonfile.close()
    csvfile.close()
    return output


def post(id, data):
    conn = http.client.HTTPSConnection('api.thingspeak.com')
    headers = {'Content-type': 'application/json'}
    conn.request('POST', '/channels/' + id + '/bulk_update.json', data, headers)
    response = conn.getresponse()
    print(response.status, response.reason)
    data = response.read()
    print(data)
    conn.close()


if __name__ == '__main__':
    auth = {'id1': '618800', 'key1': '3LG4LYDT0DY360QX', 'id2': '619384', 'key2': 'XA8NFY60KMZIJ86C', 'id3': '619385',
            'key3': 'UC9UB9W32HDAIZPH'}
    data = csv2json(filename, auth['key' + chNum])
    post(auth['id' + chNum], data)
    sys.exit()
