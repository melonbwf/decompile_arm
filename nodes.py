
#!/usr/bin/python3
# -*- coding: utf-8 -*-
#File: nodes.py
#Author: melon[melon2bwf@gmail.com]

from codes import *
from readfile import *
import os,sys,re

def find_index_by_loc(node_list, loc_string):
    for num in range(len(node_list)):
        if loc_string in node_list[num]:
            return num
    return -1

def compute_dom(codes_list, n0, N):
    '''
    # N是ANALYSE_RECORD中记录的序列集合，n0是序列集合中的起点
    # 求必经点集的算法D
    #{
    #    D(n0)={n0};
    #    for n∈N-{n0}{
    #        D(n)=N;
    #    }
    #    Flag=1;
    #    while (Flag){   
    #        Flag=0;
    #        for n∈N-{n0} {
    #            NEWD:={n}∪(D(p)的交集); p∈P(n);
    #            if (D(n)!=NEWD){
    #                Flag=1;
    #                D(n)=NEWD;
    #            }
    #        }
    #    }
    #}
    '''
    codes_list[n0].doms = {n0}
    for n in N:
        if n == n0: continue
        codes_list[n].doms = set(N)
    Flag = True
    while(Flag):
        Flag = False
        for n in N:
            if n == n0: continue
            NEWD = set(N)
            for p in codes_list[n].prevs:
                NEWD &= codes_list[p].doms
            NEWD.add(n)
            if codes_list[n].doms != NEWD:
                Flag = True
                codes_list[n].doms = NEWD


def get_route_from_s_to_e(codes_list, s, e):
    '''
    # 找到所有从start出发到end经过的结点
    # 
    # 根据回边求循环的元素算法
    # insert(m){
    #     if （m不属于loop）{
    #         m加入loop；
    #         push(m)；
    #     }
    # }
    # main(){
    #    stack = {}；
    #    loop = {d};
    #    insert(n);
    #    while (stack不空) {
    #        m = pop();
    #        p属于P(m)做： insert(p);
    #    }
    # }
    '''
    route = []
    stack = []
    route.append(s)
    if e not in route: # insert(e)
        route.append(e)
        stack.append(e)
    while len(stack) != 0:
        m = stack.pop()
        for p in codes_list[m].prevs:
            if p not in route: # insert(p)
                route.append(p)
                stack.append(p)
    return stack 

def get_loops(codes_list, N):
    # 确保已经计算过doms
    loops = []
    for i in N:
        pass        

def debug_codes_list():
    codes_list = []
    #code_type = "while" #循环类型
    code_type = "double_branch" #互交互分支
    # 互交叉分支，两个结点的prevs都是两个且相同(依据这个来判断和处理)
    if code_type == "while": #循环类型
        codes_list.append(blockcodes(0,0)) # 0
        codes_list.append(blockcodes(1,1)) # 1
        codes_list.append(blockcodes(2,2)) # 2
        codes_list.append(blockcodes(3,3)) # 3
        codes_list.append(blockcodes(4,4)) # 4
        # 添加nexts
        codes_list[0].nexts.append(1)    
        codes_list[1].nexts.append(2)
        codes_list[1].nexts.append(3)
        codes_list[2].nexts.append(1)
        codes_list[2].nexts.append(4)
        codes_list[3].nexts.append(1)
        codes_list[3].nexts.append(4)
    elif code_type == "double_branch": #互交互分支
        codes_list.append(blockcodes(0,0)) # 0
        codes_list.append(blockcodes(1,1)) # 1
        codes_list.append(blockcodes(2,2)) # 2
        codes_list.append(blockcodes(3,3)) # 3
        codes_list.append(blockcodes(4,4)) # 4
        codes_list.append(blockcodes(5,5)) # 5
        # 添加nexts
        codes_list[0].nexts.append(1)
        codes_list[0].nexts.append(2)
        codes_list[1].nexts.append(3)
        codes_list[1].nexts.append(4)
        codes_list[2].nexts.append(3)
        codes_list[2].nexts.append(4)
        codes_list[3].nexts.append(5)
        codes_list[4].nexts.append(5)

    compute_prevs(codes_list)
    compute_ancestors_and_successors(codes_list)

    return codes_list

def compute_prevs(codes_list):
    ''' 计算prevs '''
    # 先清空
    for codes in codes_list: codes.prevs.clear()
    # 再计算
    for num in range(len(codes_list)):
        for n in codes_list[num].nexts:
            if num not in codes_list[n].prevs:
                codes_list[n].prevs.append(num)

def compute_ancestors_and_successors(codes_list):
    ''' 计算 ancestors, successors '''
    # 先清空
    for codes in codes_list:
        codes.ancestors = set(codes.prevs)
        codes.successors = set(codes.nexts)
    change = True
    while change:
        change = False
        for codes in codes_list:
            for p in list(codes.ancestors):
                for pp in codes_list[p].prevs:
                    if pp not in codes.ancestors:
                        codes.ancestors.add(pp)
                        change = True
            for n in list(codes.successors):
                for nn in codes_list[n].nexts:
                    if nn not in codes.successors:
                        codes.successors.add(nn)
                        change = True
                
def init_codes_list(file_name, func_name):
    ''' '''
    codes_list = []
    if not os.path.isfile(file_name):
        return codes_list
    inputf = open(file_name)
    lines = inputf.readlines()
    inputf.close()
    
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

    # 计算prevs
    for num in range(len(codes_list)):
        for n in codes_list[num].nexts:
            if num not in codes_list[n].prevs:
                codes_list[n].prevs.append(num)

    return codes_list
    
if __name__ == '__main__':
    file_name = os.path.join(os.path.dirname(sys.argv[0]), \
                "example/loaddsp.lst")
    func_name = "sub_102FC4"

    debug = True
    try: 
        if debug:
            codes_list = debug_codes_list()
        else:
            codes_list = init_codes_list(file_name, func_name)
    except NameError:
        codes_list = init_codes_list(file_name, func_name)

    nums = [i for i in range(len(codes_list))]
    top = unknowncodes(0, nums)
    codes_list.append(top)
    compute_dom(codes_list, 0, nums)

    # dom&nexts不空,则存在回边

    for num in range(len(codes_list)):
        print("%d: %s" % (num, codes_list[num].show()))

    #print(get_route_from_s_to_e(codes_list, 0, 3))
