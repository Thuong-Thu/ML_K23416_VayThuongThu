import pickle

class FileUtil:
    @staticmethod
    def savemodel(model, filename):
        try:
            with open(filename, 'wb') as file:
                pickle.dump(model, file)
            return True
        except Exception as e:
            print("An exception occurred", e)
            return False

    @staticmethod
    def loadmodel(filename):
        try:
            with open(filename, 'rb') as file:
                model = pickle.load(file)
            return model
        except Exception as e:
            print("An exception occurred", e)
            return None
