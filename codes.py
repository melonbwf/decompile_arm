#!/usr/bin/python3
# -*- coding: utf-8 -*-  
#File: codes.py
#Aurthor: melon[melon2bwf@gmail.com]

class codes:
    def __init__(self):
        self.prevs = []
        self.nexts = []
        self.ancestors = []
        self.successors = []

    def show(self):
        print(self.prevs, self.nexts, self.ancestors, self.successors)
        
class blockcodes(codes):
    ''' blockcodes: 基本代码块,包含汇编代码行信息 '''
    def __init__(self, start=0, end=0, prevs=[], nexts=[]):
        #codes.__init__(self)
        super(blockcodes,self).__init__()
        self.start = start # 包含start
        self.end = end # 不包含end
        self.prevs = prevs
        self.nexts = nexts

    def show(self):
        return "codes[%d,%d) prevs [%s] nexts [%s]" % (self.start, self.end,
        ",".join([str(i) for i in self.prevs]),
        ",".join([str(i) for i in self.nexts]))
