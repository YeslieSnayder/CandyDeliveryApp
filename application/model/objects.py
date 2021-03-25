from datetime import datetime
import re

from application.model.exeptions import *


class Courier:
    """
    Class representing couriers:
    courier_id ->        identifier: integer >= 1
    courier_type ->      type of the courier: string in {foot, bike, car}
    regions ->           the list of regions' id in which the courier works: integer >= 1
    working_hours ->     the list of working hours of the courier {HH:MM-HH:MM}
    Additional information:
    current_order_ids -> the list that contains ids of current processing orders
    assign_time ->       appointment time of the first full order: str {1985-04-12T23:20:50.52Z}
    last_order_id ->     id of the last completed order
    orders_count ->      the map (region : number of complete orders in that region)
    """

    class TypeCourier:
        FOOT = {'name': 'foot', 'payload': 10, 'coefficient': 2}
        BIKE = {'name': 'bike', 'payload': 15, 'coefficient': 5}
        CAR = {'name': 'car', 'payload': 50, 'coefficient': 9}

    def __init__(self, json_obj):
        if Courier.is_incorrect_object_data(json_obj):
            raise WrongCourierData([json_obj['courier_id']])
        self.courier_id = json_obj['courier_id']
        self.regions = json_obj['regions']
        self.working_hours = json_obj['working_hours']

        c_type = json_obj['courier_type']
        if c_type == Courier.TypeCourier.FOOT['name']:
            self.courier_type = Courier.TypeCourier.FOOT
        elif c_type == Courier.TypeCourier.BIKE['name']:
            self.courier_type = Courier.TypeCourier.BIKE
        elif c_type == Courier.TypeCourier.CAR['name']:
            self.courier_type = Courier.TypeCourier.CAR

        if 'current_order_ids' in json_obj:
            self.current_order_ids = json_obj['current_order_ids']
        else:
            self.current_order_ids = None

        if 'assign_time' in json_obj:
            self.assign_time = json_obj['assign_time']
        else:
            self.assign_time = None

        if 'last_order_id' in json_obj:
            self.last_order_id = json_obj['last_order_id']
        else:
            self.last_order_id = None

        self.orders_count = {}
        if 'orders_count' in json_obj:
            for k in json_obj['orders_count']:
                self.orders_count[int(k)] = json_obj['orders_count'][k]
        for r in self.regions:
            if r not in self.orders_count:
                self.orders_count[r] = 0

    def __dict__(self):
        return {
            "courier_id": self.courier_id,
            "courier_type": self.courier_type['name'],
            "regions": self.regions,
            "working_hours": self.working_hours
        }

    def update(self, json_obj):
        if 'courier_type' not in json_obj and \
                'regions' not in json_obj and \
                'working_hours' not in json_obj and \
                'current_order_ids' not in json_obj and \
                'assign_time' not in json_obj and \
                'last_order_id' not in json_obj and \
                'orders_count' not in json_obj or \
                Courier.is_incorrect_data_type(json_obj):
            raise WrongCourierData([self.courier_id])

        if 'regions' in json_obj:
            self.regions = json_obj['regions']
        if 'working_hours' in json_obj:
            self.working_hours = json_obj['working_hours']
        if 'courier_type' in json_obj:
            if json_obj['courier_type'] == Courier.TypeCourier.FOOT['name']:
                self.courier_type = Courier.TypeCourier.FOOT
            elif json_obj['courier_type'] == Courier.TypeCourier.BIKE['name']:
                self.courier_type = Courier.TypeCourier.BIKE
            elif json_obj['courier_type'] == Courier.TypeCourier.CAR['name']:
                self.courier_type = Courier.TypeCourier.CAR
            else:
                raise WrongCourierData([self.courier_id])

        if 'current_order_ids' in json_obj:
            self.current_order_ids = json_obj['current_order_ids']
        if 'assign_time' in json_obj:
            self.assign_time = json_obj['assign_time']
        if 'last_order_id' in json_obj:
            self.last_order_id = json_obj['last_order_id']
        if 'orders_count' in json_obj:
            self.orders_count = json_obj['orders_count']

    @staticmethod
    def is_incorrect_object_data(data):
        if Courier.is_incorrect_data_type(data):
            return True
        return len(data) == 0 or \
            'courier_id' not in data or \
            'courier_type' not in data or \
            'regions' not in data or \
            'working_hours' not in data or \
            data['courier_id'] < 1 or \
            data['courier_type'] != Courier.TypeCourier.FOOT['name'] and \
            data['courier_type'] != Courier.TypeCourier.BIKE['name'] and \
            data['courier_type'] != Courier.TypeCourier.CAR['name']

    @staticmethod
    def is_incorrect_data_type(data):
        if 'courier_id' in data and type(data['courier_id']) != int or \
                'courier_type' in data and type(data['courier_type']) != str or \
                'regions' in data and type(data['regions']) != list or \
                'working_hours' in data and type(data['working_hours']) != list or \
                'current_order_ids' in data and data['current_order_ids'] is not None and \
                type(data['current_order_ids']) != list or \
                'assign_time' in data and data['assign_time'] is not None and \
                type(data['assign_time']) != str or \
                'last_order_id' in data and data['last_order_id'] is not None and \
                type(data['last_order_id']) != int or \
                'orders_count' in data and data['orders_count'] is not None and \
                type(data['orders_count']) != dict:
            return True
        if 'working_hours' in data:
            for hours in data['working_hours']:
                if type(hours) != str or len(hours) != 11:
                    return True
                if not re.search(r'\d{2}:\d{2}-\d{2}:\d{2}', hours):
                    return True
        if 'regions' in data:
            for region in data['regions']:
                if type(region) != int:
                    return True
                if region <= 0:
                    return True
        return False


class Order:
    """
    Class representing orders:
    order_id ->        identifier: integer >= 1
    weight ->          weight of order in kg: 0.01 <= float <= 50
    region ->          delivery area of the order: integer >= 1
    delivery_hours ->  the list of delivery time of the order {HH:MM-HH:MM}
    Additional information:
    type ->            type of order process: TypeOrder {READY, PROCESSING, COMPLETE}
    courier_id ->      identifier of courier who toke the order: integer >= 1, if 0 => no courier
    lead_time ->       time spent on that order: long int
    complete_time ->   time when the order was completed: str {1985-04-12T23:20:50.52Z}
    coefficient ->     coefficient of courier's type
    """

    class TypeOrder:
        READY = 'ready'
        PROCESSING = 'processing'
        COMPLETE = 'complete'

    def __init__(self, obj):
        if Order.is_incorrect_data_object(obj):
            raise WrongOrderData([obj['order_id']])
        self.order_id = obj['order_id']
        self.weight = obj['weight']
        self.region = obj['region']
        self.delivery_hours = obj['delivery_hours']

        if 'type' in obj:
            self.type = obj['type']
        else:
            self.type = Order.TypeOrder.READY

        if 'courier_id' in obj:
            self.courier_id = obj['courier_id']
        else:
            self.courier_id = None

        if 'lead_time' in obj:
            self.lead_time = obj['lead_time']
        else:
            self.lead_time = None

        if 'complete_time' in obj:
            if obj['complete_time'] is None:
                self.complete_time = None
            else:
                self.complete_time = obj['complete_time'].strip('"')
        else:
            self.complete_time = None

        if 'coefficient' in obj:
            self.coefficient = obj['coefficient']
        else:
            self.coefficient = None

    def __dict__(self):
        return {
            "order_id": self.order_id,
            "weight": self.weight,
            "region": self.region,
            "delivery_hours": self.region
        }

    def update(self, json_obj):
        if len(json_obj) == 0 or \
                'weight' not in json_obj and \
                'region' not in json_obj and \
                'delivery_hours' not in json_obj and \
                'type' not in json_obj and \
                'courier_id' not in json_obj and \
                'lead_time' not in json_obj and \
                'complete_time' not in json_obj and \
                'coefficient' not in json_obj:
            raise WrongOrderData([self.order_id])

        if 'weight' in json_obj:
            self.weight = json_obj['weight']
        if 'region' in json_obj:
            self.region = json_obj['region']
        if 'delivery_hours' in json_obj:
            self.delivery_hours = json_obj['delivery_hours']
        if 'type' in json_obj:
            self.type = json_obj['type']
        if 'courier_id' in json_obj:
            self.courier_id = json_obj['courier_id']
        if 'lead_time' in json_obj:
            self.lead_time = json_obj['lead_time']
        if 'complete_time' in json_obj:
            self.complete_time = json_obj['complete_time']
        if 'coefficient' in json_obj:
            self.coefficient = json_obj['coefficient']

    @staticmethod
    def is_incorrect_data_object(data):
        if len(data) == 0 or \
                'order_id' not in data or type(data['order_id']) != int or \
                'weight' not in data or (type(data['weight']) != float and type(data['weight']) != int) or \
                'region' not in data or type(data['region']) != int or \
                'delivery_hours' not in data or type(data['delivery_hours']) != list or \
                data['order_id'] < 1 or \
                data['region'] < 1 or \
                data['weight'] < 0.01 or data['weight'] > 50 or \
                len(data['delivery_hours']) == 0:
            return True
        if 'delivery_hours' in data:
            for hours in data['delivery_hours']:
                if type(hours) != str or len(hours) != 11:
                    return True
                if not re.search(r'\d{2}:\d{2}-\d{2}:\d{2}', hours):
                    return True
        return False


def get_time_from_str(str_time):
    if str_time is None or str_time == "":
        return None
    return datetime.fromisoformat(str_time[:-1] + '0000')
