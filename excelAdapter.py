import os
import xlsxwriter
import pandas as pd

class ExcelAdapter:
    def __init__(self, source):
        self.source=source

    def importData(source):
        data = pd.read_0excel(source, converters={'2G CODE final': str, '3G CODE  final': str}, sheet_name='Sheet9')
        self.data=data
        return data

    def outputData(output):
        #todo
        return
    
