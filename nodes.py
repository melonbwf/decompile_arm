#!/usr/bin/python3
# -*- coding: utf-8 -*-
#File: nodes.py
#Author: melon[melon2bwf@gmail.com]

from codes import *
from readfile import *
import os,sys,re

codes_list = []

def find_index_by_loc(node_list, loc_string):
    for num in range(len(node_list)):
        if loc_string in node_list[num]:
            return num
    return -1

if __name__ == '__main__':
    file_name = os.path.join(os.path.dirname(sys.argv[0]), \
                "example/loaddsp.lst")
    func_name = "sub_102FC4"

    inputf = open(file_name)
    lines = inputf.readlines()
    # find_func_field()返回值为list,因此需要用*将其解开
    start,end = find_func_field(lines, func_name)

    node_list = split_func_field(lines, start, end)
    #print("\n".join([str(i) for i in node_list]))

    # find_func_field()返回值为list,因此需要用*将其解开
    for node in node_list:
        codes_list.append(blockcodes(node[0], node[1]))

    for num in range(len(node_list)):
        jump_text = node_list[num][3]
        
        if jump_text == "": continue # 没有后继

        j_text, l_text = re.split(" ", jump_text)[0:2]
        #print(j_text, l_text)
        codes_list[num].nexts.append(find_index_by_loc(node_list,l_text))

        if j_text == "B": continue # 直接跳转
        codes_list[num].nexts.append(num+1)

    for num in range(len(node_list)):
        print("%d: %s" % (num, codes_list[num].show()))

    inputf.close()
