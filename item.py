#coding: utf-8
from utils.props import Props, Modifier

class Item:
  def __init__(self, ctx, props):
    self.ctx = ctx
    self.props = Props(props)
    self.modifier = Modifier()
  def getName(self):
    return self.props.get('name')
