#!/usr/bin/python3
# -*- coding: utf-8 -*-
#File: nodes.py
#Author: melon[melon2bwf@gmail.com]

from codes import *
from readfile import *
import os,sys

nodes_list = []
for node in nodes_list:
    node.show()

if __name__ == '__main__':
    #print(sys.argv[0])
    #print(os.path.dirname(sys.argv[0]))
    # loaddsp.lst和nodes.py在同一个目录
    of = open(os.path.join(os.path.dirname(sys.argv[0]),"example/loaddsp.lst"))
    lines = of.readlines()
    # find_func_field()返回值为list,因此需要用*将其解开
    nodes_list.append(blockcodes(*find_func_field(lines, "sub_102FC4")))
    for num in range(len(nodes_list)):
        print("%d: %s" % (num, nodes_list[num].show()))
