'''
@Author: Sankar
@Date: 2021-04-19 09:05:02
@Last Modified by: Sankar
@Last Modified time: 2021-05-02 09:17:09
@Title : Mapper
'''
#!/usr/bin/python

import sys

for line in sys.stdin:
    line = line.strip()
    words = line.split()
    if len(line) > 1:
        for word in words:
            print('{}\t{}'.format(word, 1))