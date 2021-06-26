import gspread
from oauth2client.service_account import ServiceAccountCredentials
import string
from datetime import datetime

_sheetid = '1UaPMiQ520CqyT-Oh12P9s8nU9fk2FjDaOfHwpGJoE1s'
_cred_file = 'betersbryggeri-72b998f0013c.json'
_worksheet = "Blad1"

def connect_sheet(sheetid, cred_file):
    sa = gspread.service_account(filename=cred_file)
    return sa.open_by_key(sheetid)

# Create new nonnection everytime for now
# TODO: Only connect when connection is lost
def connect_worksheet(worksheet_name, sheetid, cred_file):
    sheet = connect_sheet(sheetid, cred_file)
    return sheet.worksheet(worksheet_name)

def get_empty_row_idx(worksheet):
    col_vals = worksheet.col_values(1)
    return len(col_vals)+1

def get_sheet_formated_datetime(dt):
    return dt.strftime("%Y-%m-%d %H.%M.%S")

def get_range_str(row_idx, row_len):
    alphabet = list(string.ascii_uppercase)
    from_ = 'A'+str(row_idx)
    to_ = alphabet[row_len-1]+str(row_idx)
    return from_+':'+to_


# Data row contains latest data to log
def append_row(data_row, worksheet_name = _worksheet):
    worksheet = connect_worksheet(worksheet_name, _sheetid, _cred_file)
    data_row[0][0] = get_sheet_formated_datetime(data_row[0][0])
    row_idx = get_empty_row_idx(worksheet)
    range_str = get_range_str(row_idx, len(data_row[0]))
    worksheet.update(range_str, data_row)
