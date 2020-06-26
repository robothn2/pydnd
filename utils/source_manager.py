#coding: utf-8

'''
  SourceManager 管理多个 Calculator
    Calculator 可以包含多个 Source
    Calculator 可以引用多个其它 Calculator 的计算结果，这多个结果可以选择 sum 或 max 来逐一处理
      Calculator 分多种：ValueCalclator、DisableCalculator、EnableCalculator
        ValueCalclator 计算的值可以是一个 tuple，里面附带类型
  Rule 是 DND 规则，可以初始化 SourceManager 内 Source 的计算关系
    WeaponRule 用来设置武器计算规则
    UnitRule 用来设置 Unit 计算规则
'''

_preset_merge_methods = {
  'sum': lambda value1, value2: value1 + value2,
  'max': lambda value1, value2: max(value1, value2),
  'min': lambda value1, value2: min(value1, value2),
}
_preset_source_methods = {
  'modifier': lambda value: (value - 10) // 2,
}

def _translate_method(method, methodTable):
  if not method:
    return None
  if callable(method):
    return method
  return methodTable.get(method)

def _postproc_result(resultOld, resultNew, methodMerge, methodSource):
  if methodSource:
    resultNew = methodSource(resultNew)

  if resultOld is None:
    return resultNew
  if resultNew:
    return methodMerge(resultOld, resultNew)
  return resultOld # deal with resultNew == 0

class Calculator:
  def __init__(self, name, methodMerge, methodSource, kwargs):
    self._name = name
    self._upstreams = []
    self._downstreams = [] # for markDirty recursively
    self._sources = {}
    # merge result of two sources & upstreams
    self._methodMerge = _translate_method(methodMerge, _preset_merge_methods)
    if not self._methodMerge:
      self._methodMerge = _preset_merge_methods['sum']
    # affecting upstreams & sources
    self._methodSource = _translate_method(methodSource, _preset_source_methods)
    self._dirty = True
    self._noCache = kwargs.get('noCache', False)
    self._defaultResult = kwargs.get('defaultResult', 0)
    self._result = self._defaultResult

  def addDownstream(self, calculator):
    if calculator not in self._downstreams:
      self._downstreams.append(calculator)

  def addUpstream(self, calculator):
    if calculator not in self._upstreams:
      self._upstreams.append(calculator)
      self.markDirty()

  def addSource(self, sourceName, valueEstimator):
    assert(sourceName not in self._sources)
    self._sources[sourceName] = valueEstimator
    self.markDirty()

  def removeSource(self, sourceName):
    if sourceName in self._sources:
      self._sources.pop(sourceName)
      self.markDirty()

  def markDirty(self):
    if self._dirty:
      return
    self._dirty = True
    for downstream in self._downstreams:
      downstream.markDirty()

  def __call__(self, kwargs):
    if not self._dirty:
      return self._result

    result = None
    for name,estimator in self._sources.items():
      if isinstance(estimator, (int, list)):
        resultNew = estimator
      elif callable(estimator):
        resultNew = estimator(kwargs)
      else:
        continue

      result = _postproc_result(result, resultNew,
                                self._methodMerge, self._methodSource)

    for upstream in self._upstreams:
      resultNew = upstream(kwargs)
      result = _postproc_result(result, resultNew,
                                self._methodMerge, self._methodSource)
      #print(' {}: {} result: {}->{}'.format(self._name, upstream._name, resultNew, result))

    self._result = self._defaultResult if result is None else result
    if not self._noCache:
      self._dirty = False
    #print(' {} result: {}'.format(self._name, self._result))
    return self._result

class SourceManager:
  def __init__(self):
    self._calc = {}

  def addCalculator(self, name, methodMerge='sum', methodSource=None, **kwargs):
    if name not in self._calc:
      self._calc[name] = Calculator(name, methodMerge, methodSource, kwargs)

  def linkCalculator(self, upstreamName, downstreamName):
    up = self._calc.get(upstreamName)
    down = self._calc.get(downstreamName)
    if not up or not down:
      return
    up.addDownstream(down)
    down.addUpstream(up)

  def addSource(self, calculatorName, sourceName, valueEstimator):
    calculator = self._calc.get(calculatorName)
    if not calculator:
      raise RuntimeError('calculator "%s" not found' % calculatorName)
    calculator.addSource(sourceName, valueEstimator)

  def removeSource(self, calculatorName, sourceName):
    calculator = self._calc.get(calculatorName)
    if not calculator:
      raise RuntimeError('calculator "%s" not found' % calculatorName)
    calculator.removeSource(sourceName)

  def calcResult(self, calculatorName, **kwargs):
    calculator = self._calc.get(calculatorName)
    if not calculator:
      raise RuntimeError('calculator "%s" not found' % calculatorName)
    return calculator(kwargs)
