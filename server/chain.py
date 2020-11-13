import timeit
from MLFV_Constraints import MLFVConstraits

class Chain(object):
  def __init__(self, name, constraints, fn, params):
    self.name = name.replace("'", '')
    self.constr = MLFVConstraits(constraints)
    self.fn = fn
    self.params = params
  
  def run(chain):
    for imp in chain.constr.imports.split(','):
      try:
        exec('import {}'.format(imp))
      except Exception as e:
        print(e)
        return None

    # start timer
    start = timeit.default_timer()
    
    fn_params = ['{}={}'.format(key, eval(chain.params[key]) if key == 'transform' else chain.params[key]) for key in chain.params.keys()]

    # declaring params in local scope
    for param in fn_params:
      exec param
      # replacing param name with 'name=value'
      chain.fn = chain.fn.replace(param.split('=')[0], param)

    print '*********************Executing Chain*************************\n'
    print '[FUNCTION] {}'.format(chain.fn.split('(')[0])
    print '[PARAMS]'
    for param in fn_params:
      print '\t- {}'.format(param)

    chain_ret = eval(chain.fn, locals())

    # end timer
    end = timeit.default_timer()
    print '[TIME] - {} = {}\n'.format(chain.name.capitalize(), str(end - start))

    return chain_ret