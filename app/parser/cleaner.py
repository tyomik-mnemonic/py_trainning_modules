from parser.reader import WbReader
from settings.settings import settings

class Cleaner:

    def __init__(self):
        wb = WbReader(settings.data_src.path, settings.data_src.filename)
        self.wb = wb()
        
    def clean(self):
        self.active = self.wb.active
        
        for cell in list(self.active.merged_cells.ranges):
            self.active.unmerge_cells(cell.coord)
        
        for r in self.active['A1:J4']:
            print(r)
        pass
