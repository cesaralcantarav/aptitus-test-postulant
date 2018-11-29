import xlrd

def get_workbook(filename):
    return xlrd.open_workbook(filename)

def get_sheet_by_name(wb, sheet_name):
    return wb.sheet_by_name(sheet_name)

