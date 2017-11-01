import os
import tempfile
import subprocess
from ingredient_phrase_tagger.training import utils


class IngredientExtractor(object):
    def __init__(self):
        self.model_file = os.path.join(os.path.dirname(__file__), "../trained_models/model_file")

    def extract_text(self, text):
        _, cleansed_file = tempfile.mkstemp()
        with open(cleansed_file, "w") as out_file:
            out_file.write(utils.export_data(text.splitlines()))

        command = "crf_test -v 1 -m %s %s" % (self.model_file, cleansed_file)
        proc = subprocess.Popen([command], stdout=subprocess.PIPE, shell=True)
        (out, err) = proc.communicate()
        return out
