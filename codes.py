#!/usr/bin/python3
# -*- coding: utf-8 -*-  
#File: codes.py
#Aurthor: melon[melon2bwf@gmail.com]

class codes:
    def __init__(self):
        self.prevs = list()
        self.nexts = list()
        self.ancestors = set()
        self.successors = set()
        self.doms = set()

    def show(self):
        print(self.prevs, self.nexts, self.ancestors, self.successors)
        
class blockcodes(codes):
    ''' blockcodes: 基本代码块,包含汇编代码行信息 '''
    def __init__(self, start=0, end=0):
        #codes.__init__(self)
        super(blockcodes,self).__init__()
        self.start = start # 包含start
        self.end = end # 不包含end

    def show(self):
        return "codes[%d,%d) prevs [%s] nexts [%s] ance(%s), succ(%s) doms (%s)" % ( \
            self.start, self.end, \
            ",".join([str(i) for i in self.prevs]), \
            ",".join([str(i) for i in self.nexts]), \
            ",".join([str(i) for i in self.ancestors]), \
            ",".join([str(i) for i in self.successors]), \
            ",".join([str(i) for i in self.doms]))

class unknowncodes(codes):
    ''' unknowncodes: 未知代码集合 '''
    def __init__(self, head, nums):
        # head: 入口代码块序号
        # nums: 内部代码块序号集合
        super(unknowncodes,self).__init__()
        self.head = head
        self.nums = list(nums)

    def show(self):
        return "unknowncodes prevs [%s] nexts [%s] ance(%s) succ(%s) head(%s) nums(%s)" % ( \
            ",".join([str(i) for i in self.prevs]), \
            ",".join([str(i) for i in self.nexts]), \
            ",".join([str(i) for i in self.ancestors]), \
            ",".join([str(i) for i in self.successors]), \
            self.head, \
            ",".join([str(i) for i in self.nums]))
