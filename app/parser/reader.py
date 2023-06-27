import os
from settings.settings import settings
import openpyxl

class Reader:

    @staticmethod
    def read_xlxs_src():
        wb = openpyxl.load_workbook(os.path.join(settings.data_src.path, settings.data_src.filename))
        sheet = wb.active
        pass
