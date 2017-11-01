# Source code is adopted from
# https://github.com/NYTimes/ingredient-phrase-tagger/blob/master/bin/parse-ingredients.py
# https://github.com/NYTimes/ingredient-phrase-tagger/blob/master/bin/convert-to-json.py
from __future__ import print_function
import os
import tempfile
import subprocess
from ingredient_phrase_tagger.training import utils
from cStringIO import StringIO

from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage


class IngredientModel(object):
    def __init__(self):
        self.quantity = 0
        self.comment = None
        self.name = None
        self.unit = None
        self.source = None


class IngredientExtractor(object):
    def __init__(self):
        self.model_file = os.path.join(os.path.dirname(__file__), "../trained_models/model_file")

    def extract_text(self, text):
        crf_out = self.get_crf_output(text)
        json = utils.import_data(crf_out.splitlines())
        models = []
        for line in json:
            qty = line.get("qty")
            unit = line.get("unit")
            if qty is not None or unit is not None:
                model = IngredientModel()
                model.quantity = qty
                model.unit = unit
                model.name = line.get("name")
                model.comment = line.get("comment")
                model.source = line.get("input")
                models.append(model)

        return models

    def get_crf_output(self, text):
        _, cleansed_file = tempfile.mkstemp()
        with open(cleansed_file, "w") as out_file:
            out_file.write(utils.export_data(text.splitlines()))

        command = "crf_test -v 1 -m %s %s" % (self.model_file, cleansed_file)
        proc = subprocess.Popen([command], stdout=subprocess.PIPE, shell=True)
        (crf_out, err) = proc.communicate()
        os.remove(cleansed_file)
        return crf_out.decode("utf-8")

    def extract_pdf(self, pdf_file):
        rsrcmgr = PDFResourceManager()
        retstr = StringIO()
        codec = 'utf-8'
        laparams = LAParams()
        laparams.all_texts = True
        device = TextConverter(rsrcmgr, retstr, codec=codec, laparams=laparams)
        fp = open(pdf_file, 'rb')
        interpreter = PDFPageInterpreter(rsrcmgr, device)
        password = ""
        maxpages = 0
        caching = True
        pagenos = set()
        pages = PDFPage.get_pages(
            fp, pagenos, maxpages=maxpages, password=password,
            caching=caching, check_extractable=True)
        for page in pages:
            interpreter.process_page(page)
        fp.close()
        device.close()
        str = retstr.getvalue()
        retstr.close()
        return self.extract_text(str)
