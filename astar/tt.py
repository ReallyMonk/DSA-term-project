#!/usr/bin/env python
# coding=utf-8
'''
@Author: Jin X
@Date: 2020-04-10 22:16:41
@LastEditTime: 2020-04-10 22:18:14
'''


class T:
    def __init__(self):
        self.a = 'a'

    def foo(self):
        del self.a
        # del self.foo


a = T()
print(a.a)
a.foo()
print(a.a)
