from parser.reader import WbReader
from settings.settings import settings
from utils.date_setter import DateSetter
import pandas as pd

class Cleaner:

    def __init__(self):
        wb = WbReader(settings.data_src.path, settings.data_src.filename)
        self.wb = wb()
        
    def clean(self):
        self.active = self.wb.active
        
        for cell in list(self.active.merged_cells.ranges):
            self.active.unmerge_cells(cell.coord)
        dates = DateSetter().get_dates()
        for i,v in enumerate(self.active['C3:J3'][0]):
            v.value = dates[i]

        df = pd.DataFrame(self.active.values)
        pass
        
