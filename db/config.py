"""
 File contains constants for database.
 Many fields are repeating names of fields of the corresponding class.

 If you want to change structure of database,
 then you should add or remove constants in this file,
 only then change the structure of database in db-controller file
"""

DATABASE_NAME = '/home/yesliesnayder/projects/pycharmProjects/CandyDeliveryApp/model/db/database.db'

# Information about courier
COURIER_TABLE = 'couriers'

COURIER_ID = ('id', 'INTEGER PRIMARY KEY')
COURIER_TYPE = ('type', 'TEXT')
COURIER_REGIONS = ('regions', 'TEXT')                      # list
COURIER_WORKING_HOURS = ('working_hours', 'TEXT')          # list
COURIER_CURRENT_ORDER_IDS = ('current_order_ids', 'TEXT')  # list
COURIER_ASSIGN_TIME = ('assign_time', 'TEXT')
COURIER_LAST_ORDER_ID = ('last_order_id', 'INTEGER')
COURIER_ORDERS_COUNT = ('orders_count', 'TEXT')            # dict

# Information about order
ORDER_TABLE = 'orders'

ORDER_ID = ('id', 'INTEGER PRIMARY KEY')
ORDER_WEIGHT = ('weight', 'REAL')
ORDER_REGION = ('region', 'INTEGER')
ORDER_DELIVERY_HOURS = ('delivery_hours', 'TEXT')          # list
ORDER_TYPE = ('type', 'TEXT')
ORDER_COURIER_ID = ('courier_id', 'INTEGER')
ORDER_LEAD_TIME = ('lead_time', 'TEXT')
ORDER_COMPLETE_TIME = ('complete_time', 'TEXT')
ORDER_COEFFICIENT = ('coefficient', 'INTEGER')
