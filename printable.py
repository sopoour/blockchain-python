class Printable:
    #Convert the transaction objects to a dict and in order to be printable as string convert that to string
    def __repr__(self):
        return str(self.__dict__)