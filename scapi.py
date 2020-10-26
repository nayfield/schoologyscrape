

import schoolopy
import csv
import sheets_test


# get schoology api key and sec
# get hdrs for csv outputs
exec(open('config/config.py').read())

# https://github.com/ErikBoesen/schoolopy
# https://developers.schoology.com/api-documentation/rest-api-v1


# Override Schoology api limit of 20
class MySchoology(schoolopy.Schoology):
    limit = 1000



def sc_login(key, sec):
    ''' returns a Schoology object'''
    sc_obj = MySchoology(schoolopy.Auth(key, sec))
    me = sc_obj.get_me()
#    print("Logged in as:", me.name_display)
    return sc_obj

def get_kids(sc):
    '''returns a List of uids'''
    kidlist = sc.get_me().child_uids
    retval = []
    # I only have one kid.  Assuming this is a comma separated list?
    for kid in kidlist.split(','):
        retval.append(kid)
#        print(' Found Child:', sc.get_user(kid).name_display)
    return retval

def get_sections(sc, uid):
    '''returns a list of sections IDs'''
    retval = []
    for sec in sc.get_user_sections(uid):
        retval.append(sec.id)
    return retval

def get_events(sc, sec_id):
    '''returns a list of events'''
    retval = []
    cname = sc.get_section(sec_id).course_title
    mycount = 0
    for e in sc.get_section_events(sec_id):
        e['course_title'] = cname
        mycount +=1
        retval.append(e)
#    print('   Course',cname, str(mycount), 'Events.')
    return retval

def get_ass(sc, sec_id):
    '''returns a list of assignments'''
    retval = []
    cname = sc.get_section(sec_id).course_title
    mycount = 0
    for e in sc.get_assignments(sec_id):
        e['course_title'] = cname
        mycount += 1
        retval.append(e)
#    print('   Course',cname, str(mycount), 'Assignments.')
    return retval

def csv_out_all(fname, toCSV):
    '''write a complete CSV to fname given a list of dicts'''
    keysCSV = set().union(*(d.keys() for d in toCSV))
    with open(fname, 'w', newline='') as f:
        dict_writer = csv.DictWriter(f, keysCSV)
        dict_writer.writeheader()
        dict_writer.writerows(toCSV)

def csv_out_sub(fname, toCSV, fields):
    '''write a subset CSV to fname given a list of dicts and fields'''
    with open(fname, 'w', newline='') as f:
        dict_writer = csv.DictWriter(f, fields, extrasaction='ignore', )
        dict_writer.writeheader()
        dict_writer.writerows(toCSV)

def list_o_keys(lis, field):
    '''takes a list of dicts and returns a list of values of the dict field'''
    retval = []
    for k in lis:
        if field in k:
            retval.append(k[field])
    return retval

def get_uploaded_ids(sheetid, rangeid):
    ''' get the ID's (first col values) in the named sheet from google'''
    retval = []
    ssdata = sheets_test.get_sheet_range(sheetid, rangeid)
    # header row
    ssdata.pop(0)
    for row in ssdata:
        gid = row[0]
        if gid in retval:
            print("Duplicate id", gid, sheetid, rangeid)
        else:
            retval.append(gid)
    return retval

def event_to_row(ev, fields):
    ''' Take single event and return a row [list of values] for the fields'''
    retval = []
    for f in fields:
        if f in ev:
            retval.append(ev[f])
        else:
            retval.append('')
    return retval

def get_new_rows(srclist, dstids, fields):
    ''' take list o dict and return list o lists (just fields) if not in dstids'''
    retval = []
    for s in srclist:
        if str(s['id']) in dstids:
            continue
        retval.append(event_to_row(s, fields))
    return retval



if __name__ == '__main__':

    sc = sc_login(ology_key, ology_sec)
    kids = get_kids(sc)
    # I only have one kid on ology.  Removed the multi-kid code to make it easier to deal with.
    kid=kids[0]
    evs = []
    ass = []
    secs = get_sections(sc, kid)
    for s in secs:
        evs.extend(get_events(sc, s))
        ass.extend(get_ass(sc, s))

    evass = list_o_keys(evs, 'assignment_id')
    extras = []
    for a in ass:
        if a.id not in evass:
            li = dict(a)
            li['id'] = 0 - li['id']
            extras.append(li)


    in_goog = get_uploaded_ids(hw_ss_id, hw_range)
    rows = get_new_rows(evs, in_goog, ev_hdrs)
    rows.extend(get_new_rows(extras, in_goog, as_hdrs))

    if rows:
        print("New Items:", len(rows))
        # TODO add FALSE values (or checkboxes?) to end of rows?
        sheets_test.append_rows(hw_ss_id, hw_range, rows)
