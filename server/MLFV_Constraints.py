class MLFVConstraits:
    
    imports=""
    cpu=0
    mem=0
    net=0
    gpu=None

    def __init__(self, dict):
        self.imports = self.check_key(dict, 'imports', '')
        self.cpu = self.check_key(dict, 'cpu')
        self.mem = self.check_key(dict, 'mem')
        self.net = self.check_key(dict, 'net', 100)
        self.gpu = self.check_key(dict, 'gpu')

    def check_key(self, dict, key, default = 0):
        return dict[key] if dict.has_key(key) else default
