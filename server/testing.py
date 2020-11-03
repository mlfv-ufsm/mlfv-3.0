from MLFV_Constraints import MLFVConstraits


class Testing(object):        

    constr = MLFVConstraits({
        "imports": "timeit,numpy,sklearn.ensemble,sklearn.metrics",
        "cpu": 1000,
        "mem": 2,
        "net": 10
    })

    def __init__(self, pars):
        dataset, classifier = pars
        self.dataset = dataset        
        self.classifier = classifier
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

        df = numpy.array(s.dataset) 
        import cPickle as pickle, zlib as zl, base64 as b64

        c = pickle.loads(zl.decompress(b64.b64decode(s.classifier)))

        my_X = df[:, 1:]  # features
        my_Y = df[:, 0]  # actual labels

        y_pred = c.predict(my_X) #predicting

        precision,recall,fscore,support = sklearn.metrics.precision_recall_fscore_support(my_Y,y_pred)

        #end timer
        end = timeit.default_timer()
        print("[Testing time]="+str(end-start))
        print(precision,recall,fscore,support)
        return ([precision,recall,fscore,support])
    

