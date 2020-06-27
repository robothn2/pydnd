#coding: utf-8
from dice import dice_roll

'''
  SourceManager contains some Calculators provided by DND rule.
  Each Calculator contains multi sources that registered by Feat, Item, Buff,
    etc. it can also reference other Calculators, this mechnicism allows value
    computed recursively.
  Calculator uses a source method for result post-processing to sources and
    references, it also use a merge method for result merging between sources
    and references.
  Calculator can disable/enable all upstreams & sources
  A source can return value of int, tuple(2 or 3 elements) or dict:
    tuple(2): a single key-value pair
    tuple(3): a int value computed by dice roll(min, max, times)
    dict: result can be merged by key, sum values on same key
  Once upon you build up a SourceManager with rule(fill Caculators), do NOT
    call SourceManager.addCaculator() any more, instead of call addSource().
'''

_preset_merge_methods = {
  'sum': lambda value1, value2: value1 + value2,
  'max': lambda value1, value2: max(value1, value2),
  'min': lambda value1, value2: min(value1, value2),
}
_preset_source_methods = {
  'modifier': lambda value: (value - 10) // 2,
  'sum_dict': lambda d: sum(d.values()),
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
  class _IntDict(dict):
    def __add__(self, other):
      for k,v in other.items():
        if k in self:
          self[k] += int(v)
        else:
          self[k] = int(v)
      return self

  def __init__(self, name, methodMerge, methodSource, kwargs):
    self._name = name
    self._upstreams = []
    self._downstreams = [] # for markDirty recursively
    self._sources = {}
    self._enablers = []
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
    self._sourceAsEnabler = kwargs.get('sourceAsEnabler', False)

  def addDownstream(self, calculator):
    if calculator not in self._downstreams:
      self._downstreams.append(calculator)

  def addUpstream(self, calculator):
    if calculator not in self._upstreams:
      self._upstreams.append(calculator)
      self.markDirty()
      if calculator._noCache:
        self.markNoCache()

  def addSource(self, sourceName, valueEstimator):
    #print('{} add source: {}'.format(self._name, sourceName))
    if self._sourceAsEnabler:
      enabler = (sourceName, *valueEstimator)
      if enabler not in self._enablers:
        self._enablers.append(enabler)
        self._enablers.sort(key=lambda elem: elem[1], reverse=True)
        #print(self._enablers)
        self.markDirty()
    else:
      self._sources[sourceName] = valueEstimator
      self.markDirty()

  def removeSource(self, sourceName):
    if self._sourceAsEnabler:
      for i,v in enumerate(self._enablers):
        if v[0] == sourceName:
          del self._enablers[i]
          self.markDirty()
          break
    elif sourceName in self._sources:
      self._sources.pop(sourceName)
      self.markDirty()

  def markDirty(self):
    if self._dirty:
      return
    self._dirty = True
    #print('dirty: ' + self._name)
    for downstream in self._downstreams:
      downstream.markDirty()

  def markNoCache(self):
    if self._noCache:
      return
    self._noCache = True
    for up in self._upstreams:
      up.markNoCache()

  def __call__(self, kwargs):
    if not self._noCache and not self._dirty:
      return self._result

    result = None
    self._dirty = False
    if self._sourceAsEnabler:
      for enabler in self._enablers:
        #print('enabler "{}" priority({}), value({})'.format(*enabler))
        if enabler[2]:
          break; # do upstreams merging
        return self._defaultResult
    else:
      for name,estimator in self._sources.items():
        if isinstance(estimator, int):
          # support constant int or expression
          resultNew = estimator
        #elif isinstance(estimator, dict):
        #  # support multi int/tuple
        #  resultNew = Calculator._IntDict(estimator)
        elif isinstance(estimator, tuple):
          if len(estimator) == 2:
            resultNew = Calculator._IntDict()
            if isinstance(estimator[1], int):
              # support ('physical', 3)
              resultNew[estimator[0]] = estimator[1]
            elif isinstance(estimator[1], tuple):
              if not self._noCache:
                raise RuntimeError('dice tuple need noCache property on "%s"' % self._name)
              if len(estimator[1]) != 3:
                raise RuntimeError('dice tuple format error returned by "%s"' % name)
              # support ('physical', (1,6,2))
              resultNew[estimator[0]] = dice_roll(*estimator[1])
          elif len(estimator) == 3:
            # support lambda kwargs: ('physical', (1,6,2))
            resultNew = dice_roll(*estimator)
          else:
            raise RuntimeError('invalid source tuple "%s"' % name)
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
    #print(' {} result: {}'.format(self._name, self._result))
    return self._result

class SourceManager:
  def __init__(self):
    self._calc = {}

  def addCalculator(self, name, methodMerge='sum', methodSource=None, **kwargs):
    if name not in self._calc:
      self._calc[name] = Calculator(name, methodMerge, methodSource, kwargs)
    upstream = kwargs.get('upstream')
    if isinstance(upstream, str):
      self.linkCalculator(upstream, name)
    elif isinstance(upstream, (tuple, list)):
      for up in upstream:
        self.linkCalculator(up, name)

  def linkCalculator(self, upstreamName, downstreamName):
    up = self._calc.get(upstreamName)
    down = self._calc.get(downstreamName)
    if not up or not down:
      raise RuntimeError('calculator link fail "{}" -> "{}"'.format(upstreamName, downstreamName))
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
