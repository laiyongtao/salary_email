import xlrd

class ParseExcel(object):
    '''处理excel文件'''

    def __init__(self, parent=None ,file_name=None):
        ''''''

        self.parent = parent
        self.book = xlrd.open_workbook(filename=file_name)
        self.sheet = self.book.sheet_by_index(0)

        self._nrows = self.sheet.nrows  # 文件总行数
        self.nrows =  self._nrows - 1  # 文件有效行数
        self.ncols = self.sheet.ncols

        self.__headers = self.sheet.row_values(0)


    def iter_salary_line(self):
        for i in range(1,self._nrows):
            row = self.sheet.row_values(i)
            row_info = zip(self.__headers,row)
            yield list(row_info)

    @property
    def headers(self):
        return self.__headers




if __name__ == '__main__':
    p = ParseExcel(file_name='./salary来来来.xlsx')

    for i in p.iter_salary_line():
        print(i)
