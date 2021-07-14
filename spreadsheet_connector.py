import gspread
from oauth2client.service_account import ServiceAccountCredentials
import string
import datetime

from time import sleep

_sheetid = '1EestCfXucUt5knqdGMlnKy7LsTB4Oj8BkkzHQw_DCbc'
_cred_file = 'betersbryggeri-72b998f0013c.json'
_worksheet = "pifermentor"

def connect_sheet(sheetid, cred_file):
    sa = gspread.service_account(filename=cred_file)
    return sa.open_by_key(sheetid)

# Create new nonnection everytime for now
# TODO: Only connect when connection is lost
def connect_worksheet(sheetid, cred_file):
    sheet = connect_sheet(sheetid, cred_file)
    return sheet, sheet.worksheet(_worksheet)

def get_empty_row_idx_whole(worksheet):
    col_vals = worksheet.col_values(1)
    return len(col_vals)+1

def get_empty_row_idx_24h(worksheet):
    col_vals = worksheet.col_values(7)
    return len(col_vals)+1

def get_sheet_formated_datetime(dt):
    return dt.strftime("%Y-%m-%d %H.%M.%S")

def get_range_str_whole(row_idx, row_len):
    from_ = 'A'+str(row_idx)
    to_ = 'E'+str(row_idx)
    return from_+':'+to_

def get_range_str_24h(row_idx, row_len):
    from_ = 'G'+str(row_idx)
    to_ = 'K'+str(row_idx)
    return from_+':'+to_

# Filter out so only 24h remains
# Assume that alldata is sorted on time
# [[Time, temp, target, delta, on/off],
#  [...]]
def filter_24h(alldata):
    if len(alldata) == 0 or len(alldata) == 1:
        return alldata

    top_time = datetime.datetime.strptime(alldata[0][0], '%Y-%m-%d %H.%M.%S')
    latest_time = datetime.datetime.strptime(alldata[-1][0], '%Y-%m-%d %H.%M.%S')
    day_delta = datetime.timedelta(hours=24)

    #If top time plus 24h is smaller then remove top time
    cmp_time = top_time + day_delta
    if cmp_time < latest_time:
        del alldata[0]
        return filter_24h(alldata)

    return alldata

def append_row_24h(data_row, sheet=None, worksheet=None):
    if sheet == None and worksheet == None:
        sheet, worksheet = connect_worksheet(_sheetid, _cred_file)
    data_row = data_row[0]
    data_row[0] = get_sheet_formated_datetime(data_row[0])
    row_idx = get_empty_row_idx_24h(worksheet)
    range_ = 'G2:K'+str(row_idx-1 if row_idx != 2 else 2)
    alldata = worksheet.get(range_)
    alldata.append(data_row)
    alldata = filter_24h(alldata)
    sheet.values_clear(_worksheet+'!'+range_)
    range_ = 'G2:K'+str(len(alldata)+1)
    worksheet.update(range_, alldata, value_input_option='USER_ENTERED')
    return sheet, worksheet

# Data row contains latest data to log
# Time, temp, target, delta, on/off
def append_row_all(data_row, sheet=None, worksheet=None):
    if sheet == None and worksheet == None:
        sheet, worksheet = connect_worksheet(_sheetid, _cred_file)
    data_row[0][0] = get_sheet_formated_datetime(data_row[0][0])
    row_idx = get_empty_row_idx_whole(worksheet)
    range_str = get_range_str_whole(row_idx, len(data_row[0]))
    worksheet.update(range_str, data_row, value_input_option='USER_ENTERED')
    return sheet, worksheet

def clear_all():
    sheet, worksheet = connect_worksheet(_sheetid, _cred_file)
    sheet.values_clear(_worksheet+'!A2:E2000')
    sheet.values_clear(_worksheet+'!G2:K1000')

def change_beer_name(name):
    sheet, worksheet = connect_worksheet(_sheetid, _cred_file)
    worksheet.update("M12", name)

def get_beer_name():
    sheet, worksheet = connect_worksheet(_sheetid, _cred_file)
    return worksheet.acell("M12").value



#worksheet = connect_worksheet(worksheet_name, _sheetid, _cred_file)
#sheet, worksheet = connect_worksheet(_sheetid, _cred_file)
#_append_row_24h(sheet, worksheet, ["2021-06-30 23.56.11", 23, 23, 23, "ON"])
#count = 0
#while True:
#    count += 1
#    temp = 20+(count%6)
#    row = [[datetime.datetime.now(),temp, 21.5, abs(21.5-temp), 'ON']]
#    append_row(row)
#    sleep(1)
