class PpmHeader:
    def __init__(self):
        self.format = None
        self.rows = None
        self.columns = None
        self.colorScale = None

    def isComplete(self):
        return (self.format is not None and self.rows is not None
                and self.columns is not None and self.colorScale is not None)