from MLFV_Constraints import MLFVConstraits


class Testing(object):        
    constr = MLFVConstraits({
        "imports": "timeit,numpy,tensorflow",
        "cpu": 1000,
        "mem": 2,
        "net": 10
    })

    def __init__(self, pars):
        classifier, model_json, optimizer, loss, metrics, prep_data = pars
        self.classifier = classifier
        self.model_json = model_json
        self.optimizer = optimizer
        self.loss = loss
        self.metrics = metrics
        self.prep_data = prep_data
        self.name = 'Testing'
    
    def run(s):
        for i in s.constr.imports.split(','):
            try:
                exec("import "+i)
            except Exception as e:
                print(e)
                return None

        from tensorflow.keras.models import model_from_json

        #start timer
        start = timeit.default_timer()        
        print(s.name)

        import cPickle as pickle, zlib as zl, base64 as b64

        weights = pickle.loads(zl.decompress(b64.b64decode(s.classifier)))

        model = model_from_json(s.model_json)
        model.set_weights(weights)

        model.compile(optimizer=s.optimizer, loss=s.loss, metrics=s.metrics)

        print model.summary()

        _, (x_test, y_test) = s.prep_data

        results = model.evaluate(numpy.asarray(x_test), numpy.asarray(y_test), verbose=2)

        #end timer
        end = timeit.default_timer()
        print("[Testing time]="+str(end-start))
        # print(precision,recall,fscore,support)

        print results

        return results # ([precision,recall,fscore,support])
    

