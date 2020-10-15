from MLFV_Constraints import MLFVConstraits


class Selection(object):
    constr = MLFVConstraits("numpy,timeit",1000,1,10)
    
    def __init__(self,par): 
        dataset, inputs, class_name = par
        self.dataset = dataset
        self.inputs = inputs
        self.class_name = class_name
        self.name = 'Selection'

    def run(s):
        print(s.name)
        for i in s.constr.imports.split(','):
            try:
                exec("import "+i)
            except Exception as e:
                print(e)
                return None

        #start timer
        start = timeit.default_timer()

        df = numpy.array(s.dataset)

        inputs = numpy.array(s.inputs)
        inputs = numpy.append(s.class_name, s.inputs)

        data_selected = df[:, inputs]

        # stop timer
        end = timeit.default_timer()
        print("[Select time]"+str(end-start))

        return data_selected

