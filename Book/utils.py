import pickle


def save_model(model_file, model):
    with open(model_file, 'wb') as f:
        pickle.dump(model, f)


def load_model(model_file):
    with open(model_file, 'rb') as f:
        model = pickle.load(f)
        return model