from MLFV_Constraints import MLFVConstraits


class Preprocessing(object):
    constr = MLFVConstraits({
        # "imports": "timeit,numpy,sklearn.preprocessing",
        "imports": "timeit",
        "cpu": 1000,
        "mem": 2,
        "net": 10
    })

    def __init__(self, par):
        self.dataset = par[0]
        self.name = 'Preprocessing'

    def run(s):
        for i in s.constr.imports.split(','):
            try:
                exec("import "+i)
            except Exception as e:
                print(e)
                return None

        # start timer
        start = timeit.default_timer()
        print(s.name)

        (x_train, y_train), (x_test, y_test) = s.dataset

        x_train, x_test = x_train / 255.0, x_test / 255.0
        
        # end timer
        end = timeit.default_timer()
        print("[Preprocessing time]="+ str(end-start))

        return (x_train, y_train), (x_test, y_test)
