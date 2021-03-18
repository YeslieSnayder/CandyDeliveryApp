from model.objects import *
from model.db import DB
from datetime import datetime
import numpy as np


class Model:
    def __init__(self):
        self.db = DB()

    # TODO: Remove after debug
    def get_couriers(self):
        return self.db.get_couriers()

    # TODO: Remove after debug
    def get_orders(self):
        return self.db.get_orders()

    def create_couriers(self, couriers_json_list):
        wrong_ids = []
        correct_couriers = []
        for obj in couriers_json_list:
            if 'courier_id' not in obj:
                raise WrongOrderData(['Object does not have parameter "courier_id"'])
            try:
                correct_couriers.append(Courier(obj))
            except WrongCourierData as e:
                wrong_ids.append(e.args[0][0])
        if len(wrong_ids) != 0:
            raise WrongCourierData(wrong_ids)

        self.db.create_couriers(correct_couriers)
        return [c.courier_id for c in correct_couriers]

    def patch_courier(self, courier_id, courier_json):
        courier = self.get_courier(courier_id)
        try:
            courier.update(courier_json)
            self.db.update_courier(courier)
        except WrongCourierData:
            raise WrongCourierData([courier_id])
        return courier

    def get_courier(self, courier_id):
        courier = self.db.get_courier(courier_id)
        if courier is None:
            raise DataNotFound([courier_id])
        return courier

    def get_courier_full_data(self, courier_id):
        courier = self.get_courier(courier_id)
        courier_dict = courier.__dict__()
        courier_dict["earnings"] = 500 * courier.courier_type['coefficient'] * courier.delivery_count

        has_complete_orders = False
        for index, region in enumerate(courier.orders_count):
            if courier.orders_count[region] != 0:
                has_complete_orders = True
                break
        if not has_complete_orders:
            return courier_dict

        complete_orders = self.db.get_complete_orders_of_courier(courier.courier_id)
        td = np.zeros(len(complete_orders), dtype=int)
        for i in complete_orders:
            td[i.region] += i.lead_time
        for index, region in enumerate(courier.orders_count):
            if courier.orders_count[region] != 0:
                td[region] /= courier.orders_count[region]
        t = np.min(td[np.nonzero(td)])
        courier_dict['rating'] = (60 * 60 - min(t, 60 * 60)) / (60 * 60) * 5

        return courier_dict

    def get_order(self, order_id):
        order = self.db.get_order(order_id)
        if order is None:
            raise DataNotFound([order_id])
        return order

    def create_orders(self, orders_json_list):
        wrong_ids = []
        correct_orders = []
        for order in orders_json_list:
            if 'order_id' not in order:
                raise WrongOrderData(['Object does not have parameter "order_id"'])
            try:
                correct_orders.append(Order(order))
            except WrongOrderData as e:
                wrong_ids.append(e.args[0][0])
        if len(wrong_ids) != 0:
            raise WrongOrderData(wrong_ids)

        self.db.create_orders(correct_orders)
        return [o.order_id for o in correct_orders]

    def assign_order(self, courier: Courier):
        if courier is None:
            return [], None

        payload = courier.courier_type['payload']
        orders = self.db.get_orders_for_assign(courier.courier_id, payload, courier.regions, courier.working_hours)
        if len(orders) == 0:
            return [], None

        if courier.assign_time is None:
            courier.update({'assign_time': get_str_from_time(datetime.now())})

        for order in orders:
            if order.courier_id == 0 and order.type == Order.TypeOrder.READY:
                order.update({'courier_id': courier.courier_id, 'type': Order.TypeOrder.PROCESSING})
                self.db.update_order(order)

        courier.prev_order_time = courier.assign_time
        self.db.update_courier(courier)

        return [o.order_id for o in orders], courier.assign_time

    def complete_order(self, json):
        order = self.get_order(json["order_id"])
        courier = self.get_courier(json["courier_id"])
        order.complete(json, courier.prev_order_time)
        courier.prev_order_time = order.complete_time
        if courier.orders_count[order.region] is None:
            courier.orders_count[order.region] = 1
        else:
            courier.orders_count[order.region] += 1
        self.db.update_courier(courier)
        self.db.update_order(order)


def get_str_from_time(date_time):
    return date_time.isoformat()[:-4] + 'Z'


def get_time_from_str(str_time):
    return datetime.fromisoformat(str_time[:-1] + '0000')
