from model.db.sqlite_db import SQLiteDB
from model.objects import *


class Model:
    def __init__(self):
        self.db = SQLiteDB()

    def create_couriers(self, couriers_json_list):
        wrong_ids = []
        correct_couriers = []
        for obj in couriers_json_list:
            if 'courier_id' not in obj:
                raise MissingID('Object does not have parameter "courier_id"')
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
        if courier.current_order_ids is not None and ('regions' in courier_json or 'working_hours' in courier_json):
            orders = []
            for order_id in courier.current_order_ids:
                order = self.db.get_order(order_id)
                orders.append(order)
                if order.region not in courier_json['regions'] or \
                        not can_deliver_on_time(order.delivery_hours, courier.working_hours):
                    order.update({
                        'type': Order.TypeOrder.READY,
                        'courier_id': None,
                        'coefficient': None
                    })
                    self.db.update_order(order)
            for order in orders:
                courier.current_order_ids.remove(order.order_id)
        courier.update(courier_json)
        self.db.update_courier(courier)
        return courier

    def get_courier(self, courier_id):
        courier = self.db.get_courier(courier_id)
        if courier is None:
            raise DataNotFound([courier_id])
        return courier

    def get_courier_full_data(self, courier_id):
        courier = self.get_courier(courier_id)
        courier_dict = courier.__dict__()
        orders = self.db.get_complete_orders_of_courier(courier_id)

        sum_coefficients = 0
        processing_time_in_regions = {}
        for order in orders:
            sum_coefficients += order.coefficient
            if order.region in processing_time_in_regions:
                processing_time_in_regions[order.region] += order.lead_time
            else:
                processing_time_in_regions[order.region] = order.lead_time

        courier_dict["earnings"] = 500 * sum_coefficients

        if sum_coefficients == 0:
            return courier_dict

        for region in processing_time_in_regions:
            processing_time_in_regions[region] = processing_time_in_regions[region] / courier.orders_count[region]

        t = min(processing_time_in_regions.values())
        courier_dict['rating'] = round((60 ** 2 - min(t, 60 ** 2)) / 60 ** 2 * 5, 2)
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
                raise MissingID('Object does not have parameter "order_id"')
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

        if courier.current_order_ids is not None and len(courier.current_order_ids) > 0:
            return courier.current_order_ids, courier.assign_time

        payload = courier.courier_type['payload']
        orders = self.db.get_orders_for_assign(payload, courier.regions)
        if len(orders) == 0:
            return [], None

        orders = list(filter(
            lambda order_item: can_deliver_on_time(order_item.delivery_hours, courier.working_hours), orders))
        orders.sort(key=lambda o: o.weight)
        load_sum = 0
        courier.current_order_ids = []
        for order in orders:
            if load_sum + order.weight > payload:
                break
            courier.current_order_ids.append(order.order_id)
            order.update({
                'courier_id': courier.courier_id,
                'type': Order.TypeOrder.PROCESSING,
                'coefficient': courier.courier_type['coefficient']
            })
            load_sum += order.weight
            self.db.update_order(order)

        courier.update({'assign_time': get_str_from_time(datetime.now())})
        self.db.update_courier(courier)

        return courier.current_order_ids, courier.assign_time

    def complete_order(self, json):
        order = self.get_order(json['order_id'])
        courier = self.get_courier(json['courier_id'])

        if courier.current_order_ids is None or \
                order.order_id not in courier.current_order_ids or \
                order.courier_id != courier.courier_id:
            raise WrongCourierData([json['courier_id']])

        if courier.last_order_id is None:
            last_order_time = courier.assign_time
        else:
            last_order = self.get_order(courier.last_order_id)
            last_order_time = last_order.complete_time
        process_time = (get_time_from_str(json['complete_time']) - get_time_from_str(last_order_time)).total_seconds()

        order.update({
            'type': Order.TypeOrder.COMPLETE,
            'lead_time': process_time,
            'complete_time': json['complete_time']
        })
        courier.current_order_ids.remove(order.order_id)
        courier.update({'last_order_id': order.order_id})

        if order.region in courier.orders_count:
            courier.orders_count[order.region] += 1
        else:
            courier.orders_count[order.region] = 1
        self.db.update_courier(courier)
        self.db.update_order(order)


def can_deliver_on_time(delivery_time: list, working_hours: list):
    """
    The method checks the delivery time that should be in boundary of working hours.
    :param delivery_time: delivery time of an order.
    :param working_hours: working hours of a courier.
    :return: True - if delivery time falls under working hours,
    otherwise - False.
    """
    for del_time in delivery_time:
        delivery_start = datetime.strptime(del_time[:5], '%H:%M')
        delivery_end = datetime.strptime(del_time[6:], '%H:%M')

        for work_time in working_hours:
            work_start = datetime.strptime(work_time[:5], '%H:%M')
            work_end = datetime.strptime(work_time[6:], '%H:%M')
            if work_start < delivery_end and delivery_start < work_end:
                return True
    return False


def get_str_from_time(date_time):
    return date_time.isoformat()[:-4] + 'Z'


def get_time_from_str(str_time):
    return datetime.fromisoformat(str_time[:-1] + '0000')
