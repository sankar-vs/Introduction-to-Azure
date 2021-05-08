'''
@Author: Sankar
@Date: 2021-05-02 09:13:25
@Last Modified by: Sankar
@Last Modified time: 2021-05-02 09:17:09
@Title : Reducer
'''
#!/usr/bin/python

import sys

lastkey = None
current = 0

for line in sys.stdin:
    line = line.strip()
    key, value = line.split('\t')
    try:
        value = int(value)
        if key != lastkey:
            if lastkey is not None:
                print('{}\t{}'.format(lastkey, current))
            lastkey = key
            current = 0
        current += 1
    except ValueError:
        pass

if lastkey is not None:
    print('{}\t{}'.format(lastkey, current))