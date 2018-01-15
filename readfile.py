#!/usr/bin/python3
# -*- coding: utf-8 -*-
#File: readfile.py
#Author: melon[melon2bwf@gmail.com]

import re,os,sys
 
# [文件预处理]
# 第一步: IDA->Produce file->Create LST file... 生成loaddsp.lst
# 第二步: UltraEdit-32 另存为 格式:ANSI/ASCII 覆盖loaddsp.lst
# 第三步: Notepad++, 正则表达式替换, 去除不必要的内容
#       1. "; End of	function" -> "End of	function"
#       2. "[ \t]+;.*$" --> ""
#       3. "^\." --> ""
#       4. "^[a-z]+:[0-9A-F]+$" -> ""
#       5. "^[a-z]+:" -> ""
#       6. "[ \t]+" -> " "
#       7. Notepad++ 编辑->行操作->移除空行(包括空白字符)

# 获取指定函数的起始行和终止行
# 起始行：00102FC4 sub_102FC4
# 终止行: 00103BF8 End of function sub_102FC4
def find_func_field(lines, func_name):
    length = len(lines)
    start_pattern = re.compile("[0-9A-F]+ %s" % func_name)
    for start in range(length):
        if start_pattern.match(lines[start]): break
    end_pattern = re.compile("[0-9A-F]+ End of function %s" % func_name)
    for end in range(length):
        if end_pattern.match(lines[end]): break
    if start==length-1 or end==length-1:
        return 0,0
    return start,end

if __name__ == '__main__':
    of = open(os.path.join(os.path.dirname(sys.argv[0]),"example/loaddsp.lst"))
    lines = of.readlines()
    # find_func_field()返回值为list,因此需要用*将其解开
    start,end = find_func_field(lines, "sub_102FC4")
    print(start,end)
    new_lines = lines[start:end]
    # 找出所有分割代码块的依据:loc_XXXX或locret_XXXX
    loc_list = []
    loc_pattern = re.compile("[0-9A-F]+ [loc_|locret_]")
    for num in range(len(new_lines)):
        if loc_pattern.match(new_lines[num]):
            loc_list.append([num+start, re.split(' ',new_lines[num].strip(" \r\n"))[1]])
    #print(loc_list)
    # 找到所有跳转的位置
    jump_pattern = re.compile("[0-9A-F]+ B.* loc")
    for num in range(len(new_lines)):
        if jump_pattern.match(new_lines[num]):
            tmp = re.split(' ',new_lines[num].strip(" \r\n"))[1:]
            tmp.insert(0, num+start)
            loc_list.append(tmp)
    loc_list = sorted(loc_list, key=lambda d: d[0])
    #print("\n".join([str(i) for i in loc_list]))
    current = start
    node_list = []
    for loc in loc_list: # loc[0]是分割点
        if loc[0] == current: continue # 已经分割了，不用处理该点
        if len(loc) == 2: # loc_XXXX:
            node_list.append([current, loc[0]])
            current = loc[0]
        else: # B loc_XXXX
            node_list.append([current, loc[0]+1])
            current = loc[0]+1
    if current != end:
        node_list.append([current, end])
    for node in node_list:
        first = lines[node[0]].strip(" \r\n")
        first_split = re.split(" ",first)
        if not first_split[1].startswith("loc"):
            first = "" # 不是loc_XXXX信息的，直接舍弃
        else:
            first = " ".join(first_split[1:]) # 去掉地址信息
        last = lines[node[1]-1].strip(" \r\n")
        last_split = re.split(" ",last)
        if len(last_split)<3 or \
           not last_split[1].startswith("B") or \
           not last_split[2].startswith("loc"):
            last = "" # 不是跳转语句，直接舍弃
        else:
            last = " ".join(re.split(" ",last)[1:]) # 去掉地址信息
        node.append(first)
        node.append(last)
    print("\n".join([str(i) for i in node_list]))
