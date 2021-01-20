from MLFV_Constraints import MLFVConstraits

class Training(object):
    constr = MLFVConstraits({
        "imports": "timeit,numpy,tensorflow",
        "cpu": 1000,
        "mem": 2,
        "net": 10
    })

    def __init__(self, pars):
        model_json, custom_layers, optimizer, loss, metrics, prep_data = pars
        self.model_json = model_json
        self.custom_layers = custom_layers
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

        import keras

        print s.custom_objects['SpatialPyramidPooling'].__dict__

        # start timer
        start = timeit.default_timer()
        print(s.name)

        (x_train, y_train), _ = s.prep_data
        
        model = keras.models.model_from_json(
            s.model_json,
            custom_objects = (
                s.custom_objects
                    if hasattr(s, 'custom_objects')
                    else {}
            )
        )

        model.compile(optimizer=s.optimizer, loss=s.loss, metrics=s.metrics)

        print model.summary()

        model.fit(numpy.asarray(x_train), numpy.asarray(y_train), epochs=5)

        # end timer
        end = timeit.default_timer()
        print("[Training time]="+ str(end-start))

        return model.get_weights()

