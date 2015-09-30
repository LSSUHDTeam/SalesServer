__author__ = 'jbosley2'

import sql_selects as SELECT
import sql_inserts as INSERT
import sql_updates as UPDATE

def request_handler(request):

    info = []

    # ===================[ SELECT QUERIES ]===================
    if request[0] == 's':

        # Select All Receipts
        if request[1] == 'ar':
            info = SELECT.select_receipts_by_descriptor(request[2], request[3])

        # Select Inventory
        if request[1] == 'ai':
            info = SELECT.select_inventory()

        if request[1] == 'inf':
            info = SELECT.select_sales_information()

        if request[1] == "dinf":
            info = SELECT.select_department_information()

        if request[1] == "lgn":
            info = SELECT.check_user_information(request)

        if request[1] == "rbmy":
            info = SELECT.select_receipt_for_report_by_month_year(request[2])

        if request[1] == "rfdc":
            info = SELECT.select_receipts_for_drawer_close()

        if request[1] == "cbdr":
            info = SELECT.select_closings_by_date_range(request[2])

        if request[1] == "rbi":
            info = SELECT.select_receipts_by_id_range(request[2])



    # ===================[ INSERT QUERIES ]===================
    if request[0] == 'i':

        if request[1] == 'nr':

            info = INSERT.new_receipt(request[2])

        if request[1] == 'nii':

            info = INSERT.new_inventory_item(request[2])

        if request[1] == 'inc':

            info = INSERT.insert_new_closing(request[2])

    # ====================[ UPDATE QUERIES ]==================

   # precision

    if request[0] == 'u':

        if request[1] == 'rbi':

            info = UPDATE.update_receipt_by_id(request)

        if request[1] == 'ibi':

            info = UPDATE.update_item_by_id(request[2])

        if request[1] == 'dibi':

            info = UPDATE.delete_item_by_id(request[2])

        if request[1] == 'rdel':

            info = UPDATE.delete_receipt_by_id(request[2])

        if request[1] == "cbi":

            info = UPDATE.closing_by_id(request)

    data_send = []
    for el in info:
        data_send.append(el.replace('\n', ''))
    # Used to show the end of transfer
    data_send.append('\n')
    return ''.join(data_send)
