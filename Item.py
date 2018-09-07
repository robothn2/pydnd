#coding: utf-8
import warnings
from common import Props

class Item:
    def __init__(self, ctx, props):
        self.ctx = ctx
        self.props = Props.Props(props)
        self.modifier = Props.Modifier()
