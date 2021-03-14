from model.exeptions import *
import numpy as np
from datetime import datetime


class Courier:
    """
    Class representing couriers:
    courier_id ->    identifier: integer >= 1
    courier_type ->  type of the courier: string in {foot, bike, car}
    regions ->       the list of regions' id in which the courier works: integer >= 1
    working_hours -> the list of working hours of the courier {HH:MM-HH:MM}
    Additional information:
    td ->            the list of average delivery time in regions (element [i] => region number 'i')
    orders_count ->  the list of number of complete orders in regions (element [i] => region number 'i')
    orders_done ->   the list of complete orders in regions (element [i] => region number 'i')
    assign_time ->   appointment time of the first orders: Date {YYYY-MM-DDThh:mm:ss[.SS]Z : 1985-04-12T23:20:50.52Z}
    status ->        status of the courier: bool {true - in processing of delivery, false - chill}
    """

    class TypeCourier:
        FOOT = {'name': 'foot', 'payload': 10, 'coefficient': 2}
        BIKE = {'name': 'bike', 'payload': 15, 'coefficient': 5}
        CAR = {'name': 'car', 'payload': 50, 'coefficient': 9}

    def __init__(self, json_obj, td=None, orders_count=None, orders_done=None, status=False):
        if not Courier.is_correct_object_data(json_obj):
            raise WrongCourierData([json_obj['courier_id']])
        self.courier_id = json_obj['courier_id']
        self.courier_type = json_obj['courier_type']
        self.regions = json_obj['regions']
        self.working_hours = json_obj['working_hours']
        self.assign_time = None
        self.status = status
        if td is None:
            self.td = np.array([])
        else:
            self.td = td
        if orders_count is None:
            self.orders_count = np.array([])
        else:
            self.orders_count = orders_count
        if orders_done is None:
            self.orders_done = np.array([])
        else:
            self.orders_done = orders_done

    def __dict__(self):
        return {
            "courier_id": self.courier_id,
            "courier_type": self.courier_type,
            "regions": self.regions,
            "working_hours": self.working_hours
        }

    def __str__(self):
        return str(self.__dict__())

    def update(self, json_obj):
        if 'courier_id' in json_obj \
                or 'courier_type' not in json_obj \
                and 'regions' not in json_obj \
                and 'working_hours' not in json_obj \
                and 'assign_time' not in json_obj \
                and 'status' not in json_obj:
            raise WrongCourierData()

        if 'regions' in json_obj:
            self.regions = json_obj['regions']
        if 'working_hours' in json_obj:
            self.working_hours = json_obj['working_hours']
        if 'assign_time' in json_obj:
            self.assign_time = json_obj['assign_time']
        if 'status' in json_obj:
            self.status = json_obj['status']
        if 'courier_type' in json_obj:
            if json_obj['courier_type'] == Courier.TypeCourier.FOOT['name'] \
                    or json_obj['courier_type'] == Courier.TypeCourier.BIKE['name'] \
                    or json_obj['courier_type'] == Courier.TypeCourier.CAR['name']:
                self.courier_type = json_obj['courier_type']
            else:
                raise WrongCourierData()

    def get_data(self):
        res = self.__dict__()
        t = np.min(self.td)
        res['rating'] = (60*60 - min(t, 60*60))/(60*60) * 5

    @staticmethod
    def is_correct_object_data(data):
        if len(data) != 4 \
                or 'courier_id' not in data or type(data['courier_id']) != int \
                or 'courier_type' not in data or type(data['courier_type']) != str \
                or 'regions' not in data or type(data['regions']) != list \
                or 'working_hours' not in data or type(data['working_hours']) != list \
                or data['courier_id'] < 1 \
                or data['courier_type'] != Courier.TypeCourier.FOOT['name'] \
                and data['courier_type'] != Courier.TypeCourier.BIKE['name'] \
                and data['courier_type'] != Courier.TypeCourier.CAR['name']:
            return False
        return True


class Order:
    """
    Class representing orders:
    order_id ->        identifier: integer >= 1
    weight ->          weight of order in kg: 0.01 <= float <= 50
    region ->          delivery area of the order: integer >= 1
    delivery_hours ->  the list of delivery time of the order {HH:MM-HH:MM}
    Additional information:
    type ->            type of order process: TypeOrder {READY, PROCESSING, COMPLETE}
    complete_time ->   time when the order was completed: Date {YYYY-MM-DDThh:mm:ss[.SS]Z : 1985-04-12T23:20:50.52Z}
    courier_id ->      identifier of courier who toke the order: integer >= 1, if 0 => no courier
    """

    class TypeOrder:
        READY = 0
        PROCESSING = 1
        COMPLETE = 2

    def __init__(self, obj):
        if not Order.is_correct_data_object(obj):
            raise WrongOrderData([obj['order_id']])
        self.order_id = obj['order_id']
        self.weight = obj['weight']
        self.region = obj['region']
        self.delivery_hours = obj['delivery_hours']
        self.type = Order.TypeOrder.READY
        self.complete_time = None
        self.courier_id = 0

    def update(self, json_obj):
        if len(json_obj) == 0 \
                or 'weight' not in json_obj \
                and 'region' not in json_obj \
                and 'delivery_hours' not in json_obj \
                and 'type' not in json_obj \
                and 'complete_time' not in json_obj \
                and 'courier_id' not in json_obj:
            raise WrongOrderData()

        if 'weight' in json_obj:
            self.weight = json_obj['weight']
        if 'region' in json_obj:
            self.region = json_obj['region']
        if 'delivery_hours' in json_obj:
            self.delivery_hours = json_obj['delivery_hours']
        if 'type' in json_obj:
            self.type = json_obj['type']
        if self.type == Order.TypeOrder.PROCESSING and 'complete_time' in json_obj:
            self.complete_time = json_obj['complete_time']
        if self.type != Order.TypeOrder.READY and 'courier_id' in json_obj:
            self.courier_id = json_obj['courier_id']

    def complete(self, json):
        if json["courier_id"] != self.courier_id:
            raise WrongCourierData([json["courier_id"]])
        if self.type == Order.TypeOrder.READY:
            raise WrongOrderData([json['order_id']])
        if self.type == Order.TypeOrder.PROCESSING:
            self.update(json)

    @staticmethod
    def is_correct_data_object(data):
        if len(data) != 4 \
                or 'order_id' not in data or type(data['order_id']) != int \
                or 'weight' not in data or (type(data['weight']) != float and type(data['weight']) != int) \
                or 'region' not in data or type(data['region']) != int \
                or 'delivery_hours' not in data or type(data['delivery_hours']) != list \
                or data['order_id'] < 1 \
                or data['region'] < 1 \
                or data['weight'] < 0.01 or data['weight'] > 50:
            return False
        return True
