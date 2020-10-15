class MLFVConstraits:
    
    imports=""
    cpu=0
    mem=0
    net=0

    def __init__(self, imports, cpu, mem, net):
        self.imports = imports
        self.cpu = cpu
        self.mem = mem
        self.net = net
