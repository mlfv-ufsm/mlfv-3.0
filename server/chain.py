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
    
    fn_params = ','.join(['{}={}'.format(key, eval(chain.params[key]) if key == 'transform' else chain.params[key]) for key in chain.params.keys()])

    print '*********************Executing Chain*************************\n'
    print '[FUNCTION] {}({})'.format(chain.fn.split('(')[0], fn_params)

    chain_ret = eval('{}({})'.format(chain.fn, fn_params))

    print chain_ret

    # end timer
    end = timeit.default_timer()
    print '[TIME] - {} = {}\n'.format(chain.name.capitalize(), str(end - start))

    return chain_ret