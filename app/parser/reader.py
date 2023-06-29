import os
from settings.settings import settings
import openpyxl

class WbReader:

    def __init__(self, path:str, name:str):
        self.path = path
        self.name = name

    def __call__(self):
        self.wb = openpyxl.load_workbook(
            os.path.join(
                self.path,
                self.name
            )
        )
        return self.wb

    @staticmethod
    def read_xlxs_src():
        wb = openpyxl.load_workbook(
            os.path.join(
                settings.data_src.path, 
                settings.data_src.filename
            )
        )
        sheet = wb.active
        pass
