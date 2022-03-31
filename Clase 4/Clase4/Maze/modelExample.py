from model import Model

class ModelExample(Model):

    def __init__(self, model_file):
        super().__init__(model_file)
        self.reset()
        relative_path = 'gym_maze/envs/maze_samples/'
        self._load_model(relative_path + model_file)

    def _load_model(self, fullpath):
        print("Load your model here with file:", fullpath)
        with open(str(fullpath), 'r') as f:
            self._raw_model = list(f)

