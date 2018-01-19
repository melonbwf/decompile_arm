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
    ''' 
    函数汇编起始段: XXXX <func_name>
    函数汇编结束段: XXXX End of function <func_name>
    '''
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


def split_func_field(lines, start, end):
    '''
    # 根据loc_XXXX和BXX loc_XXXX分割汇编代码，形成基本代码块
    # 返回值: [块首行号,块尾行号,
    #            块首loc_XXXX信息(如果有), 块尾BXX loc_XXXX信息(如果有)]
    '''
    new_lines = lines[start:end]
    # 找出所有分割代码块的依据:loc_XXXX或locret_XXXX
    loc_list = []
    loc_pattern = re.compile("[0-9A-F]+ [loc_|locret_]")
    for num in range(len(new_lines)):
        if loc_pattern.match(new_lines[num]):
            loc_list.append([num+start, "head"]) # 块首
    #print(loc_list)
    # 找到所有跳转的位置
    jump_pattern = re.compile("[0-9A-F]+ B.* loc")
    for num in range(len(new_lines)):
        if jump_pattern.match(new_lines[num]):
            loc_list.append([num+start, "tail"]) # 块尾
    # 根据行号排序
    loc_list = sorted(loc_list, key=lambda d: d[0])
    #print("\n".join([str(i) for i in loc_list]))

    current = start # 当前分割点
    node_list = []
    for loc in loc_list: # loc[0]是行号
        if loc[0] == current: continue # 已经分割了，不用处理该点
        if loc[1] == "head": # 块首
            node_list.append([current, loc[0]])
            current = loc[0]
        else: # 块尾
            node_list.append([current, loc[0]+1])
            current = loc[0]+1
    if current != end:
        node_list.append([current, end])

    # 添加块首和块尾语句信息
    for node in node_list:
        line_split = re.split(" ",lines[node[0]].strip(" \r\n"))
        if not line_split[1].startswith("loc"):
            first = "" # 不是loc_XXXX信息的，直接舍弃
        else:
            first = line_split[1] # 只记录loc_XXXX信息

        line_split = re.split(" ",lines[node[1]-1].strip(" \r\n"))
        if len(line_split)<3 or \
           not line_split[1].startswith("B") or \
           not line_split[2].startswith("loc"):
            last = "" # 不是跳转语句，直接舍弃
        else:
            last = " ".join(line_split[1:3]) # 去掉地址信息

        node.append(first)
        node.append(last)

    #print("\n".join([str(i) for i in node_list]))
    return node_list

if __name__ == '__main__':
    file_name = os.path.join(os.path.dirname(sys.argv[0]), \
                "example/loaddsp.lst")
    func_name = "sub_102FC4"

    inputf = open(file_name)
    lines = inputf.readlines()
    # find_func_field()返回值为list,因此需要用*将其解开
    start,end = find_func_field(lines, func_name)

    node_list = split_func_field(lines, start, end)
    print("\n".join([str(i) for i in node_list]))

    inputf.close()
