from MLFV_Constraints import MLFVConstraits


class Preprocessing(object):
    constr = MLFVConstraits({ "imports": "timeit,numpy,sklearn.preprocessing", "cpu": 1000, "mem": 2, "net": 10 })

    def __init__(self, par):
        dataset, scaler = par
        self.dataset = dataset
        self.scaler = scaler
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
        
        df = numpy.array(s.dataset) 
        x = df[:,1:]
        y = df[:,0]

        if s.scaler == 'Standard':
            sc = sklearn.preprocessing.StandardScaler()
        elif s.scaler == 'MinMax':
            sc = sklearn.preprocessing.MinMaxScaler()

        x_scaled = sc.fit_transform(x)
        x_norm = x_scaled

        new_df = numpy.column_stack((y,x_norm))

        # end timer
        end = timeit.default_timer()
        print("[Preprocessing time]="+ str(end-start))

        return new_df
