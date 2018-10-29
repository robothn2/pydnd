#coding: utf-8
from common import Props
from Dice import rollDice
import Apply

class Item:
    def __init__(self, ctx, props):
        self.ctx = ctx
        self.props = Props.Props(props)
        self.modifier = Props.Modifier()
    def getName(self):
        return self.props.get('name')
