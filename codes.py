#!/usr/bin/python3
# -*- coding: utf-8 -*-  
#File: codes.py
#Aurthor: melon[melon2bwf@gmail.com]

class codes:
    def __init__(self):
        self.prevs = list()
        self.nexts = list()
        self.ancestors = list()
        self.successors = list()
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
        return "codes[%d,%d) prevs [%s] nexts [%s] doms (%s)" % (self.start, self.end,
        ",".join([str(i) for i in self.prevs]),
        ",".join([str(i) for i in self.nexts]),
        ",".join([str(i) for i in self.doms]))
