from MLFV_Constraints import MLFVConstraits


class Testing(object):        
    constr = MLFVConstraits({
        "imports": "timeit,numpy,tensorflow",
        "cpu": 1000,
        "mem": 2,
        "net": 10
    })

    def __init__(self, pars):
        self.classifier = pars[0]
        self.name = 'Testing'
    
    def run(s):
        for i in s.constr.imports.split(','):
            try:
                exec("import "+i)
            except Exception as e:
                print(e)
                return None


        #start timer
        start = timeit.default_timer()        
        print(s.name)


        mnist = tensorflow.keras.datasets.mnist

        (x_train, y_train), (x_test, y_test) = mnist.load_data()

        import cPickle as pickle, zlib as zl, base64 as b64

        c = pickle.loads(zl.decompress(b64.b64decode(s.classifier)))

        print c

        #end timer
        end = timeit.default_timer()
        print("[Testing time]="+str(end-start))
        # print(precision,recall,fscore,support)
        return ([precision,recall,fscore,support])
    

