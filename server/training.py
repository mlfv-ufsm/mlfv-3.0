from MLFV_Constraints import MLFVConstraits

class Training(object):
    constr = MLFVConstraits({
        "imports": "timeit,numpy,tensorflow",
        "cpu": 1000,
        "mem": 2,
        "net": 10
    })

    def __init__(self, pars):
        model_json, optimizer, loss, metrics, prep_data = pars
        self.model_json = model_json
        self.optimizer = optimizer
        self.loss = loss
        self.metrics = metrics
        self.prep_data = prep_data
        self.name = 'Training'
    
    def run(s):
        for i in s.constr.imports.split(','):
            try:
                exec("import " + i)
            except Exception as e:
                print(e)
                return None

        # start timer
        start = timeit.default_timer()
        print(s.name)

        (x_train, y_train), _ = s.prep_data

        model = tensorflow.keras.models.model_from_json(s.model_json)
        model.compile(optimizer=s.optimizer, loss=s.loss, metrics=s.metrics)

        print model.summary()

        model.fit(numpy.asarray(x_train), numpy.asarray(y_train), epochs=5)

        # end timer
        end = timeit.default_timer()
        print("[Training time]="+ str(end-start))

        return model.get_weights()

