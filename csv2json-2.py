#!/usr/bin/python
# Filename: csv2json-2.py
# Author: Zixiang Nie (znie@ufl.edu)
# Modified Nov 10 2018
# Reduce the size of json file, to run in raspberry pies.
# Remove lines share same MAC in one second.

import sys
import csv
import json
import collections

filename = sys.argv[1]


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


if __name__ == '__main__':
    csv2json(filename, 'key')
