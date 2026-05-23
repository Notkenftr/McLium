from mclium.context import MemoryContext
class Memory:
    def __init__(self):
        self.this_identifier = None
        self.this_memory = {}

    def set_identifier(self, identifier ,name="unknown"):
        if len(identifier.__str__()) < 6:
            raise ValueError("Identifier is too short.")

        self.this_identifier = identifier

        MemoryContext().identifier[self.this_identifier] = [self.this_identifier,name]

    def insert_data(self, data):
        if self.this_identifier is None:
            raise ValueError("Identifier is not set.")
        if self.this_memory is None:
            self.this_memory = {}

        self.this_memory[self.this_identifier] = data
        MemoryContext().memory[self.this_identifier] = self.this_memory

    def get_identifier(self):
        return self.this_identifier

    def get_data(self,identifier=None):
        if identifier:
            return MemoryContext().identifier[identifier], MemoryContext().memory[identifier]

        if self.this_identifier is None:
            raise ValueError("Identifier is not set.")
        return MemoryContext().memory[self.this_identifier]

#test
if __name__ == '__main__':
    mc = MemoryContext()
    mc.init()

    m = Memory()
    m.set_identifier(1321685)
    m.insert_data("abc")
    print(m.get_data())
