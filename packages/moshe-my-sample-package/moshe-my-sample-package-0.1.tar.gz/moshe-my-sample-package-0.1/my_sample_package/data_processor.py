class DataProcessor:
    def __init__(self, data):
        self.data = data

    def sum(self):
        return sum(self.data)

    def average(self):
        return sum(self.data) / len(self.data) if self.data else 0
