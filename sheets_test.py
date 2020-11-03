
# example google auth and test code.
# should be able to execute this file and auth once
# https://developers.google.com/sheets/api/reference/rest/v4/spreadsheets.values/append


import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import re





# If modifying these scopes, delete the file token.pickle.
G_SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

# Source config vars.
exec(open('config/config.py').read())



def goog_creds():
    """Simple google example to get credentials.
    returns creds suitable for googleapis.
    """

    # Token file (created automatically)
    tokfile = 'config/token.pickle'

    # Credential JSON key (obtained from Google)
    credfile = 'config/credentials.json'


    creds = None

    if os.path.exists(tokfile):
        with open(tokfile, 'rb') as token:
            creds = pickle.load(token)

    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(credfile, G_SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open(tokfile, 'wb') as token:
            pickle.dump(creds, token)

    return creds




def get_sheet_range(sheet_id, sheet_range):
    """Shows basic usage of the Sheets API.
    Prints values from a sample spreadsheet.
    """
    creds = goog_creds()

    service = build('sheets', 'v4', credentials=creds)

    # Call the Sheets API
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=sheet_id,
                                range=sheet_range).execute()
    values = result.get('values', [])

    return values

def append_rows(sheet_id, sheet_range, vals):

    creds = goog_creds()

    body = {'values': vals}

    service = build('sheets', 'v4', credentials=creds)

    # Call the Sheets API
    sheet = service.spreadsheets()
    result = sheet.values().append(spreadsheetId=sheet_id,
                                    range=sheet_range,
                                   valueInputOption='USER_ENTERED', body=body).execute()
    count = result.get('UpdatedCells')

    return result

def add_col(c, n):
    '''Add or subtract columns.  TODO make work beyond Z (AA)'''
    return chr(ord(c) + n)

def ext_range(up, ncols):
    '''given a range spec, return a range of ncols more columns'''
    #print(type(up))
    if '!' in up:
        retval, range = up.split('!')
        retval = retval + '!'
    else:
        retval = ''
        range = up

    ost, oen = re.findall('(\w+?)(\d+)', range)

    retval = retval + add_col(oen[0], 1) + ost[1] + ':'
    retval = retval + add_col(oen[0], ncols) + oen[1]
    return retval

def insChk(ss, range):
    print('HUMAN!  Add checkboxes to {} range {}'.format(ss, range))
    # TODO implement

    return True

if __name__ == '__main__':
    # Running this file will get stuff from a sample google sheet.
    # Useful if you need to auth.  Get config/credentials.json first.

    SAMPLE_SPREADSHEET_ID = '1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms'
    SAMPLE_RANGE_NAME = 'Class Data!A2:E'
    values = get_sheet_range(SAMPLE_SPREADSHEET_ID, SAMPLE_RANGE_NAME)
    if not values:
        print('No data found.')
    else:
        print('Name, Major:')
        for row in values:
            # Print columns A and E, which correspond to indices 0 and 4.
            print('%s, %s' % (row[0], row[4]))
