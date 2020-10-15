from MLFV_Constraints import MLFVConstraits

class Training(object):        
    constr = MLFVConstraits("timeit,numpy,sklearn.ensemble",1000,2,10)
        
    def __init__(self, pars):
        dataset, classifier, cla_opts = pars
        self.dataset = dataset        
        self.classifier = classifier
        self.cla_opts = cla_opts       
        self.name = 'Training'
    
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

        # Allow other classifiers
        if s.classifier == "RF":
            classif= sklearn.ensemble.RandomForestClassifier(n_estimators=s.cla_opts)
        
        # In the training file, the classes' labels are in the first column
        labels = df[:,0]
        # The other columns are features
        features = df[:,1:]

        #print "  Fitting classifier..."
        c = classif.fit(features, labels)

        # end timer
        end = timeit.default_timer()
        print("[Training time]="+ str(end-start))

        return c
    

