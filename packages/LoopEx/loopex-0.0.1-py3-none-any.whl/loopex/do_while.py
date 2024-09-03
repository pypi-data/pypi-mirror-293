class LoopEx:
    def __init__(self):
        self.index = 0

    def do_while(self, condition):
        r = True if self.index == 0 else condition
        self.index += 1
        return r
