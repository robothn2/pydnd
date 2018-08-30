#coding: utf-8

class Object(dict):
    def __init__(self, **kwargs):
        super(Object, self).__init__(kwargs)
