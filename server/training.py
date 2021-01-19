from MLFV_Constraints import MLFVConstraits

class Training(object):
    constr = MLFVConstraits({
        "imports": "timeit,numpy,tensorflow",
        "cpu": 1000,
        "mem": 2,
        "net": 10
    })

    def __init__(self, pars):
        optimizer, loss, metrics = pars
        self.optimizer = optimizer
        self.loss = loss
        self.metrics = metrics
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

        mnist = tensorflow.keras.datasets.mnist

        (x_train, y_train), (x_test, y_test) = mnist.load_data()
        x_train, x_test = x_train / 255.0, x_test / 255.0

        model = tensorflow.keras.models.Sequential([
            tensorflow.keras.layers.Flatten(input_shape=(28, 28)),
            tensorflow.keras.layers.Dense(128, activation='relu'),
            tensorflow.keras.layers.Dropout(0.2),
            tensorflow.keras.layers.Dense(10, activation='softmax')
        ])

        model.compile(optimizer=s.optimizer, loss=s.loss, metrics=s.metrics)

        c = model.fit(x_train, y_train, epochs=5)

        model.save('trained_model.h5')

        print('Model saved!')

        # end timer
        end = timeit.default_timer()
        print("[Training time]="+ str(end-start))

        return c 

