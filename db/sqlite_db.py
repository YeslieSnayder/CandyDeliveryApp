import json
import sqlite3

from db.__init__ import *
from model.objects import *
from db.db_interface import DB


class SQLiteDB(DB):
    def __init__(self):
        """
        Initialization of the database.
        Important point: All non-standard data types such as list and dict
        are stored in database with type TEXT, later they will be parsed by json.
        """
        super().__init__()
        try:
            with sqlite3.connect(DATABASE_NAME) as con:
                cursor = con.cursor()

                sql = f'CREATE TABLE IF NOT EXISTS {COURIER_TABLE}(' \
                      f'{COURIER_ID[0]} {COURIER_ID[1]}, ' \
                      f'{COURIER_TYPE[0]} {COURIER_TYPE[1]}, ' \
                      f'{COURIER_REGIONS[0]} {COURIER_REGIONS[1]}, ' \
                      f'{COURIER_WORKING_HOURS[0]} {COURIER_WORKING_HOURS[1]}, ' \
                      f'{COURIER_CURRENT_ORDER_IDS[0]} {COURIER_CURRENT_ORDER_IDS[1]}, ' \
                      f'{COURIER_ASSIGN_TIME[0]} {COURIER_ASSIGN_TIME[1]}, ' \
                      f'{COURIER_LAST_ORDER_ID[0]} {COURIER_LAST_ORDER_ID[1]}, ' \
                      f'{COURIER_ORDERS_COUNT[0]} {COURIER_ORDERS_COUNT[1]})'
                cursor.execute(sql)

                sql = f'CREATE TABLE IF NOT EXISTS {ORDER_TABLE}(' \
                      f'{ORDER_ID[0]} {ORDER_ID[1]}, ' \
                      f'{ORDER_WEIGHT[0]} {ORDER_WEIGHT[1]}, ' \
                      f'{ORDER_REGION[0]} {ORDER_REGION[1]}, ' \
                      f'{ORDER_DELIVERY_HOURS[0]} {ORDER_DELIVERY_HOURS[1]}, ' \
                      f'{ORDER_TYPE[0]} {ORDER_TYPE[1]}, ' \
                      f'{ORDER_COURIER_ID[0]} {ORDER_COURIER_ID[1]}, ' \
                      f'{ORDER_LEAD_TIME[0]} {ORDER_LEAD_TIME[1]}, ' \
                      f'{ORDER_COMPLETE_TIME[0]} {ORDER_COMPLETE_TIME[1]}, ' \
                      f'{ORDER_COEFFICIENT[0]} {ORDER_COEFFICIENT[1]})'
                cursor.execute(sql)
        except sqlite3.Error as e:
            print('SQLite error:', e)

    def create_couriers(self, courier_list):
        """
        The method imports all couriers from input list to the database.
        :param courier_list: a list that contains objects of type 'Courier'.
        :return: True - creation was successful, otherwise - False.
        """
        try:
            with sqlite3.connect(DATABASE_NAME) as con:
                cursor = con.cursor()

                cursor.execute(f'SELECT {COURIER_ID[0]} FROM {COURIER_TABLE}')
                ids = [row[0] for row in cursor.fetchall()]

                for courier in courier_list:
                    regions = json.dumps(courier.regions)
                    working_hours = json.dumps(courier.working_hours)
                    if courier.courier_id in ids:
                        values = [courier.courier_type['name'], regions, working_hours]
                        sql = f'''UPDATE {COURIER_TABLE} SET 
                                         {COURIER_TYPE[0]} = ? ,
                                         {COURIER_REGIONS[0]} = ? ,
                                         {COURIER_WORKING_HOURS[0]} = ? 
                                  WHERE  {COURIER_ID[0]} = {courier.courier_id}'''
                        cursor.execute(sql, list(values))
                    else:
                        order_ids = json.dumps(courier.current_order_ids)
                        assign_time = json.dumps(courier.assign_time)
                        last_order_id = json.dumps(courier.last_order_id)
                        orders_count = json.dumps(courier.orders_count)
                        values = (courier.courier_id, courier.courier_type['name'], regions, working_hours,
                                  order_ids, assign_time, last_order_id, orders_count)
                        sql = f'INSERT INTO {COURIER_TABLE} VALUES {values}'
                        cursor.execute(sql)
        except sqlite3.Error as e:
            print('SQLite error:', e)
            return False
        return True

    def create_orders(self, order_list):
        """
        The method imports all orders from input list to the database.
        :param order_list: a list that contains objects of type 'Order'.
        :return: True - creation was successful, otherwise - False.
        """
        try:
            with sqlite3.connect(DATABASE_NAME) as con:
                cursor = con.cursor()

                cursor.execute(f'SELECT {ORDER_ID[0]} FROM {ORDER_TABLE}')
                ids = [row[0] for row in cursor.fetchall()]

                for order in order_list:
                    delivery_hours = json.dumps(order.delivery_hours)
                    if order.order_id in ids:
                        values = [order.weight, order.region, delivery_hours]
                        sql = f'''UPDATE {ORDER_TABLE} SET 
                                         {ORDER_WEIGHT[0]} = ? ,
                                         {ORDER_REGION[0]} = ? ,
                                         {ORDER_DELIVERY_HOURS[0]} = ? 
                                  WHERE  {ORDER_ID[0]} = {order.order_id}'''
                        cursor.execute(sql, list(values))
                    else:
                        courier_id = json.dumps(order.courier_id)
                        lead_time = json.dumps(order.lead_time)
                        complete_time = json.dumps(order.complete_time)
                        coefficient = json.dumps(order.coefficient)
                        values = (order.order_id, order.weight, order.region, delivery_hours,
                                  order.type, courier_id, lead_time, complete_time, coefficient)
                        sql = f'INSERT INTO {ORDER_TABLE} VALUES {values}'
                        cursor.execute(sql)
        except sqlite3.Error as e:
            print('SQLite error:', e)
            return False
        return True

    def update_courier(self, courier: Courier):
        """
        The method updates data of courier in database by replacing it with new object.
        :param courier: new object of type 'Courier' that will replace the previous
        object in database that has the same id.
        :return: True - updating was successful, otherwise - False
        """
        try:
            with sqlite3.connect(DATABASE_NAME) as con:
                cursor = con.cursor()

                regions = json.dumps(courier.regions)
                working_hours = json.dumps(courier.working_hours)
                order_ids = json.dumps(courier.current_order_ids)
                assign_time = json.dumps(courier.assign_time)
                last_order_id = json.dumps(courier.last_order_id)
                orders_count = json.dumps(courier.orders_count)
                values = (courier.courier_type['name'], regions, working_hours,
                          order_ids, assign_time, last_order_id, orders_count)
                sql = f'''UPDATE {COURIER_TABLE} SET 
                                 {COURIER_TYPE[0]} = ? ,
                                 {COURIER_REGIONS[0]} = ? ,
                                 {COURIER_WORKING_HOURS[0]} = ? ,
                                 {COURIER_CURRENT_ORDER_IDS[0]} = ? ,
                                 {COURIER_ASSIGN_TIME[0]} = ? ,
                                 {COURIER_LAST_ORDER_ID[0]} = ? ,
                                 {COURIER_ORDERS_COUNT[0]} = ? 
                          WHERE  {COURIER_ID[0]} = {courier.courier_id}'''
                cursor.execute(sql, values)
        except sqlite3.Error as e:
            print('SQLite error:', e)
            return False
        return True

    def update_order(self, order: Order):
        """
        The method updates data of order in database by replacing it with new object.
        :param order: new object of type 'Order' that will replace the previous
        object in database that has the same id.
        :return: True - updating was successful, otherwise - False
        """
        try:
            with sqlite3.connect(DATABASE_NAME) as con:
                cursor = con.cursor()

                delivery_hours = json.dumps(order.delivery_hours)
                courier_id = json.dumps(order.courier_id)
                lead_time = json.dumps(order.lead_time)
                complete_time = json.dumps(order.complete_time)
                coefficient = json.dumps(order.coefficient)
                values = (order.weight, order.region, delivery_hours,
                          order.type, courier_id, lead_time, complete_time, coefficient)
                sql = f'''UPDATE {ORDER_TABLE} SET 
                                 {ORDER_WEIGHT[0]} = ? ,
                                 {ORDER_REGION[0]} = ? ,
                                 {ORDER_DELIVERY_HOURS[0]} = ? ,
                                 {ORDER_TYPE[0]} = ? ,
                                 {ORDER_COURIER_ID[0]} = ? ,
                                 {ORDER_LEAD_TIME[0]} = ? ,
                                 {ORDER_COMPLETE_TIME[0]} = ? ,
                                 {ORDER_COEFFICIENT[0]} = ? 
                          WHERE  {ORDER_ID[0]} = {order.order_id}'''
                cursor.execute(sql, values)
        except sqlite3.Error as e:
            print('SQLite error:', e)
            return False
        return True

    def get_courier(self, courier_id):
        """
        The method returns the object of type 'Courier' that has id from the input.
        :param courier_id: id of courier in database that should be returned.
        :return: if courier with given id exists in the database => the object of type 'Courier'
        otherwise => None
        """
        try:
            with sqlite3.connect(DATABASE_NAME) as con:
                cursor = con.cursor()

                cursor.execute(f'SELECT * FROM {COURIER_TABLE} WHERE {COURIER_ID[0]} = {courier_id}')
                values = cursor.fetchone()
                if values is None:
                    return None
                return parse_sql_to_courier(values)
        except sqlite3.Error as e:
            print('SQLite error:', e)
            return None

    def get_order(self, order_id):
        """
        The method returns the object of type 'Order' that has id from the input.
        :param order_id: id of order in database that should be returned.
        :return: if order with given id exists in the database => the object of type 'Order'
        otherwise => None
        """
        try:
            with sqlite3.connect(DATABASE_NAME) as con:
                cursor = con.cursor()

                cursor.execute(f'SELECT * FROM {ORDER_TABLE} WHERE {ORDER_ID[0]} = {order_id}')
                values = cursor.fetchone()
                if values is None:
                    return None
                return parse_sql_to_order(values)
        except sqlite3.Error as e:
            print('SQLite error:', e)
            return None

    def get_complete_orders_of_courier(self, courier_id):
        """
        The method returns the list of orders that were completed by courier with id from input.
        :param courier_id: id of a courier that completed the orders.
        :return: the list of orders that were completed by courier with id (courier_id).
        """
        try:
            with sqlite3.connect(DATABASE_NAME) as con:
                cursor = con.cursor()

                cursor.execute(f'SELECT * FROM {ORDER_TABLE} WHERE '
                               f'{ORDER_COURIER_ID[0]} = {courier_id} AND '
                               f'{ORDER_TYPE[0]} = {json.dumps(Order.TypeOrder.COMPLETE)}')
                return [parse_sql_to_order(row) for row in cursor.fetchall()]
        except sqlite3.Error as e:
            print('SQLite error:', e)
            return []

    def get_orders_for_assign(self, courier_payload, courier_regions):
        """
        The method returns a list of orders that are satisfied by conditions for assigning.
        It checks the region of order, the weight, delivery time,
        and returns the list of the orders.
        :param courier_payload: the maximum payload of the courier.
        :param courier_regions: the regions where courier is working.
        :return: the list with the orders for a courier.
        """
        try:
            with sqlite3.connect(DATABASE_NAME) as con:
                cursor = con.cursor()
                regions = str(json.dumps(courier_regions)).replace('[', '(').replace(']', ')')

                sql = f'''SELECT * FROM {ORDER_TABLE} 
                          WHERE {ORDER_REGION[0]} IN {regions} AND 
                                {ORDER_WEIGHT[0]} <= {courier_payload} AND 
                                {ORDER_TYPE[0]} = {json.dumps(Order.TypeOrder.READY)}'''
                cursor.execute(sql)
                return [parse_sql_to_order(row) for row in cursor.fetchall()]
        except sqlite3.Error as e:
            print('SQLite error:', e)
            return []


def parse_sql_to_courier(sql):
    """
    Parses a tuple with data from database to an object of type 'Courier'.
    :param sql: tuple with complete data (length = 8).
    :return: object of type 'Courier'.
    """
    lo_id = sql[6]
    if lo_id is not None:
        lo_id = str(lo_id)
    params = {
        'courier_id': sql[0],
        'courier_type': sql[1],
        'regions': json.loads(sql[2]),
        'working_hours': json.loads(sql[3]),
        'current_order_ids': json.loads(sql[4]),
        'assign_time': json.loads(sql[5]),
        'last_order_id': json.loads(lo_id),
        'orders_count': json.loads(sql[7])
    }
    return Courier(params)


def parse_sql_to_order(sql):
    """
    Parses a tuple with data from database to an object of type 'Order'.
    :param sql: tuple with complete data (length = 9).
    :return: object of type 'Order'.
    """
    r, c_id, c_time, coef = sql[2], sql[5], sql[7], sql[8]
    if r is not None:
        r = str(r)
    if c_id is not None:
        c_id = str(c_id)
    if coef is not None:
        coef = str(coef)
    if c_time == 'null':
        c_time = None
    params = {
        'order_id': sql[0],
        'weight': sql[1],
        'region': json.loads(r),
        'delivery_hours': json.loads(sql[3]),
        'type': sql[4],
        'courier_id': json.loads(c_id),
        'lead_time': json.loads(sql[6]),
        'complete_time': c_time,
        'coefficient': json.loads(coef)
    }
    return Order(params)
