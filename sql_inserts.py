__author__ = 'jbosley2'

import settings as SQLS


def new_receipt(data):
    info = []
    cells = data.split("|")

    # Create Receipt
    SQLS.db_update(
        "INSERT INTO receipts "
        "(dateCreated, seller, firstName, lastName, itemsSold, totalPrice,"
        " description, deptCode, transactionType, transactionCode )"
        "VALUES"
        "('%s','%s','%s','%s','%s',%s,'%s','%s','%s','%s');" %
        (cells[0], cells[1], cells[2], cells[3], cells[4], cells[5], cells[6], cells[7], cells[8], cells[9])
    )

    # Send back new receipt id for the printed receipt

    if cells[1] != "DAILY RECEIPT" :

        try:
            info.append(str(SQLS.db_fetch("SELECT receiptId FROM receipts WHERE dateCreated = '%s';" % cells[0])[0][0]))
        except:
            info.append("1")

    # Update the quantity of the item in the inventory
    for item in cells[4].split(","):

        new_quantity = -1
        item_id = item.split("#")[0]
        item_quantity = item.split("#")[1]

        current_item_quantity = SQLS.db_fetch(
            "SELECT quantity FROM inventory WHERE inventoryId = '%s';" % item_id
        )[0][0]

        new_quantity = int(current_item_quantity) - int(item_quantity)

        if new_quantity != -1:

            SQLS.db_update(
                "UPDATE inventory SET quantity = %s WHERE inventoryId = '%s';" % (new_quantity, item_id)
            )

    SQLS.output_update_to_screen("Inserted new receipt . . . ")
    return info


def new_inventory_item(itemDetails):

    info = []
    cells = itemDetails.split("|")
    try:
        SQLS.db_update(
            "INSERT INTO inventory "
            "(itemName, description, price, quantity, deal, quickSaleId)"
            "VALUES"
            "('%s', '%s', '%s', '%s', '%s', -1);" %
            (cells[0], cells[1], cells[2], cells[3], cells[4])
        )
        info.append("1")
    except:
        info.append("-1")
    SQLS.output_update_to_screen("Inserted new item into inventory . . . ")
    return info

def insert_new_closing(update):

    info = []
    cells = update.split("|")

    info.append(str(SQLS.db_update(
        "INSERT INTO closings"
        "(startDate, endDate, calculatedAmount, drawerAmount, comments)"
        "VALUES"
        "('%s','%s','%s','%s','%s')" %
        (cells[0], cells[1], cells[2], cells[3], cells[4])
    )))

    SQLS.output_update_to_screen("Inserted new close . . . . . ")
    return info