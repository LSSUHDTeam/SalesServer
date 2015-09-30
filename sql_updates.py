__author__ = 'jbosley2'

import settings as SQLS


def update_receipt_by_id(request):

    info = []
    cells = request[2].split("|")
    original_data = SQLS.db_fetch("SELECT * FROM receipts WHERE receiptId = %s;" % cells[0])[0]

    # Add quantities to inventory of items originally on receipt
    for el in original_data[5].split(","):
        item_id = el.split("#")[0]
        quantity = int(el.split("#")[1])
        current_item_quantity = int(SQLS.db_fetch("SELECT quantity FROM inventory WHERE inventoryId = %s;"
                                                  % item_id)[0][0])
        updated_quantity = current_item_quantity + quantity
        SQLS.db_update("UPDATE inventory SET quantity = %s WHERE inventoryId = %s;" % (updated_quantity, item_id))

    # Update receipt information
    SQLS.db_update("UPDATE receipts SET seller = '%s', firstName = '%s', lastName = '%s', itemsSold = '%s',"
                   "totalPrice = %s, description = '%s', deptCode = '%s', transactionType = '%s', "
                   "transactionCode = '%s' WHERE receiptId = %s;" %
                   (cells[2], cells[3], cells[4],
                    cells[5], cells[6], cells[7],
                    cells[8], cells[9], cells[10],
                    cells[0]))

    # Go through each inventory item and update quantity in db
    for el in cells[5].split(","):
        item_id = el.split("#")[0]
        quantity = int(el.split("#")[1])
        current_item_quantity = int(SQLS.db_fetch("SELECT quantity FROM inventory WHERE inventoryId = %s;"
                                                  % item_id)[0][0])
        updated_quantity = current_item_quantity - quantity

        if updated_quantity < 0:
            updated_quantity = 0

        SQLS.db_update("UPDATE inventory SET quantity = %s WHERE inventoryId = %s;" % (updated_quantity, item_id))

    info.append("1")
    return info


def update_item_by_id(request):

    info = []

    cells = request.split("|")

    info.append(str(SQLS.db_update(
        "UPDATE inventory SET itemName = '%s', description = '%s', price = %s, quantity = %s, deal = '%s'"
        "WHERE inventoryId = %s;" % (cells[1], cells[2], cells[3], cells[4], cells[5], cells[0])
    )))

    return info


def delete_item_by_id(id):

    info = []

    info.append(str(SQLS.db_update(
        "DELETE FROM inventory WHERE inventoryId = %s;" % id
    )))
    return info


def delete_receipt_by_id(id):

    # Get items from receipt
    items_sold = ""
    try:
        items_sold = SQLS.db_fetch(
            "SELECT itemsSold FROM receipts WHERE receiptId = %s;" % id
        )[0][0]
    except:
        SQLS.output_update_to_screen("Unable to fetch items sold in receipt id : %s ." % id )

    # Add their quantities back into inventory
    if items_sold != "":

        for el in items_sold.split(","):

            item_id = el.split("#")[0]
            quantity = int(el.split("#")[1])

            # If the item isn't a general library item, update quantity
            if item_id != "94":
                current_item_quantity = int(SQLS.db_fetch("SELECT quantity FROM inventory WHERE inventoryId = %s;"
                                                          % item_id)[0][0])
                updated_quantity = current_item_quantity + quantity

                SQLS.db_update("UPDATE inventory SET quantity = %s WHERE inventoryId = %s;" %
                               (updated_quantity, item_id))
            else:
                # If it is a general lib item, set to 0
                SQLS.db_update("UPDATE inventory SET quantity = %s WHERE inventoryId = 0;")

    # Delete receipt
    info = []
    info.append(str(SQLS.db_update(
        "DELETE FROM receipts WHERE receiptId = %s;" % id
    )))

    return info


def closing_by_id(request):

    info = []
    id = request[2]
    cells = request[3].split("|")

    info.append(str(SQLS.db_update(
        "UPDATE closings SET startDate = '%s', endDate = '%s', "
        "calculatedAmount = %s, drawerAmount = %s, comments = '%s'"
        "WHERE idclosings = %s;" % (cells[0], cells[1], cells[2], cells[3], cells[4], id)
    )))

    SQLS.output_update_to_screen("Edited closing : %s" % id )
    return info

