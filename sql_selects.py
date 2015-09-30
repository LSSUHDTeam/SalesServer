__author__ = 'jbosley2'

import datetime

import settings as SQLS

# Range of dates
def select_receipts_by_descriptor(range, switch):

    info = []
    first_date = range.split("|")[0]
    second_date = range.split("|")[1]

    query = ""
    if switch == "1":
        query = ("SELECT * FROM receipts "
                 "WHERE transactionType != 'CHARGE BACK' "
                 "AND DATE(dateCreated) between DATE('%s') AND DATE('%s');" %
                (first_date, second_date))

    if switch == "2":
        query = ("SELECT * FROM receipts "
                 "WHERE transactionType = 'CHARGE BACK' "
                 "AND DATE(dateCreated) between DATE('%s') AND DATE('%s');" %
                (first_date, second_date))


    if switch == "3":
        query = ("SELECT * FROM receipts "
                 "WHERE DATE(dateCreated) between DATE('%s') AND DATE('%s');" %
                (first_date, second_date))

    try:
        for el in SQLS.db_fetch(query):
            for ell in el:
                info.append( str(ell).replace('\n', ''))
                info.append("|")
            info.append("%")
        info.pop(-1)
        if info[-1] == "|":
            info.pop(-1)
    except:
        info.append("NA")

    print info

    SQLS.output_update_to_screen("Request for receipts between %s , and %s  -> " % (first_date, second_date))
    return info


def select_inventory():

    info = []
    try:
        for el in SQLS.db_fetch("SELECT * FROM inventory WHERE quantity > 0 OR price = 0 ORDER BY itemName;"):
            for ell in el:
                info.append(str(ell))
                info.append("|")
            info.append("%")
        info.pop(-1)
        if info[-1] == "|":
            info.pop(-1)
    except:
        info.append("NA")

    SQLS.output_update_to_screen("Request for inventory list.  -> ")
    return info


def select_sales_information():

    info = []
    for el in SQLS.db_fetch("SELECT * FROM information WHERE idinformation = 0;"):
        for ell in el:
            info.append(str(ell))
            info.append("|")
    info.pop(-1)

    SQLS.output_update_to_screen("Request for sales information.  -> ")
    return info


def select_department_information():

    info = []
    try:
        for el in SQLS.db_fetch("SELECT * FROM departmentInformation ORDER BY deptName;"):
            for ell in el:
                info.append(str(ell))
                info.append("|")
            info.append("%")
        info.pop(-1)
        if info[-1] == "|":
            info.pop(-1)
    except:
        info.append("NA")

    SQLS.output_update_to_screen("Request for department list.  -> ")
    return info


def select_receipt_for_report_by_month_year(request):

    month = request.split("|")[0]
    year = request.split("|")[1]

    info = []
    try:


        for el in SQLS.db_fetch(
             "SELECT * "
                "FROM receipts "
                "WHERE MONTH(dateCreated) = %s "
                "AND YEAR(dateCreated) = %s "
                "AND transactionType = '%s' "
                "ORDER BY deptCode;" % (month, year, "CHARGE BACK")
        ):
            for ell in el:
                info.append(str(ell))
                info.append("|")
            info.append("%")
        info.pop(-1)
        if info[-1] == "|":
            info.pop(-1)
    except:
        info.append("NA")

    SQLS.output_update_to_screen("Request for report by month and year .  -> ")
    return info


def check_user_information(request):
    info = []
    user_id = SQLS.db_fetch("SELECT username FROM userAccess WHERE username = '%s';" % request[2])
    if len(user_id) > 0:
        user_id = user_id[0][0]
        password = SQLS.db_fetch("SELECT password FROM userAccess WHERE username = '%s';" % user_id)[0][0]
        if password == request[3]:
            info.append("1")
            return info
    else:
        info.append("3")
        return info
    info.append("2")
    return info

def select_receipts_for_drawer_close():

    # This will get the date from today, and select
    info = []

    try:
        last_close_id = SQLS.db_fetch("SELECT max(idclosings) FROM closings;")[0][0]
    except:
        print " UNABLE TO OBTAIN ID OF LAST CLOSE DATE "

    try:
        last_close_date = SQLS.db_fetch("SELECT endDate FROM closings WHERE idclosings = %s;" % last_close_id)[0][0]
    except:
        print " UNABLE TO OBTAIN THE MOST RECENT CLOSE DATE "

    info.append(str(last_close_date))
    info.append("%")

    now = datetime.datetime.now()

    try:
        for el in SQLS.db_fetch("SELECT * FROM receipts WHERE dateCreated between '%s' AND '%s';" %
                               (last_close_date, now)):
            for ell in el:
                info.append(str(ell))
                info.append("|")
            info.append("%")
        info.pop(-1)
        if info[-1] == "|":
            info.pop(-1)
    except:
        info.append("NA")

    return info


def select_closings_by_date_range(dates):

    info = []

    try:
        for el in SQLS.db_fetch("SELECT * FROM closings WHERE DATE(endDate) between '%s' AND '%s' "
                                "AND comments != 'START_MARKER';" %
                               (dates.split("|")[0], dates.split("|")[1])):
            for ell in el:
                info.append(str(ell))
                info.append("|")
            info.append("%")
        info.pop(-1)
        if info[-1] == "|":
            info.pop(-1)
    except:
        info.append("NA")

    return info


def select_receipts_by_id_range(range):

    info = []
    try:
        for el in SQLS.db_fetch("SELECT * FROM receipts WHERE receiptId between '%s' AND '%s';" %
                               (range.split("|")[0], range.split("|")[1])):
            for ell in el:
                info.append(str(ell))
                info.append("|")
            info.append("%")
        info.pop(-1)
        if info[-1] == "|":
            info.pop(-1)
    except:
        info.append("NA")

    return info

