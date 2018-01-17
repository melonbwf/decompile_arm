
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
            if num not in codes_list[n].prevs: codes_list[n].prevs.append(num)

    return codes_list
    
if __name__ == '__main__':
    file_name = os.path.join(os.path.dirname(sys.argv[0]), \
                "example/loaddsp.lst")
    func_name = "sub_102FC4"

    codes_list = init_codes_list(file_name, func_name)
    compute_dom(codes_list, 0, [i for i in range(len(codes_list))])

    for num in range(len(codes_list)):
        print("%d: %s" % (num, codes_list[num].show()))

    print(get_route_from_s_to_e(codes_list, 0, 90))
