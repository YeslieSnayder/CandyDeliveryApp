from model.objects import *


class Model:
    def __init__(self):
        self.couriers = []
        self.orders = []

    def add_courier(self, courier_json):
        c = Courier(courier_json)
        self.couriers.append(c)

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

        for courier in correct_couriers:
            self.couriers.append(courier)
        return [c.courier_id for c in correct_couriers]

    def patch_courier(self, courier_id, courier_json):
        courier = self.get_courier(courier_id)
        if courier is None:
            raise DataNotFound([courier_id])
        try:
            courier.update(courier_json)
        except WrongCourierData:
            raise WrongCourierData([courier_id])
        return courier

    def get_courier(self, courier_id):
        courier_list = list(filter(lambda i: i.courier_id == courier_id, self.couriers))
        if len(courier_list) == 0:
            raise DataNotFound([courier_id])
        return courier_list[0]

    def get_order(self, order_id):
        order_list = list(filter(lambda i: i.order_id == order_id, self.orders))
        if len(order_list) == 0:
            raise DataNotFound([order_id])
        return order_list[0]

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

        for order in correct_orders:
            self.orders.append(order)
        return [o.order_id for o in correct_orders]

    def assign_order(self, courier):
        if courier is None:
            return [], None

        if courier.courier_type == Courier.TypeCourier.FOOT['name']:
            payload = Courier.TypeCourier.FOOT['payload']
        elif courier.courier_type == Courier.TypeCourier.BIKE['name']:
            payload = Courier.TypeCourier.BIKE['payload']
        elif courier.courier_type == Courier.TypeCourier.CAR['name']:
            payload = Courier.TypeCourier.CAR['payload']
        else:
            raise WrongCourierData(courier.courier_id)

        orders = list(filter(lambda order: order.region in courier.regions
                                           and order.weight <= payload
                                           and can_deliver_on_time(order.delivery_hours, courier.working_hours)
                                           and (order.type == Order.TypeOrder.READY
                                                or order.type == Order.TypeOrder.PROCESSING
                                                and order.courier_id == courier.courier_id),
                             self.orders))
        if len(orders) == 0:
            return [], None

        if courier.assign_time is None:
            courier.update({'assign_time': get_str_from_time(datetime.now())})
        for o in orders:
            if o.courier_id == 0 and o.type == Order.TypeOrder.READY:
                o.update({'courier_id': courier.courier_id, 'type': Order.TypeOrder.PROCESSING})
        return [o.order_id for o in orders], courier.assign_time

    def complete_order(self, json):
        order = self.get_order(json["order_id"])
        order.complete(json)


def can_deliver_on_time(delivery_time, working_hours):
    for del_time in delivery_time:
        delivery_start = datetime.strptime(del_time[:5], '%H:%M')
        delivery_end = datetime.strptime(del_time[6:], '%H:%M')

        for work_time in working_hours:
            work_start = datetime.strptime(work_time[:5], '%H:%M')
            work_end = datetime.strptime(work_time[6:], '%H:%M')
            if delivery_start <= work_start < delivery_end or delivery_start < work_end <= delivery_end:
                return True
    return False


def get_str_from_time(date_time):
    return date_time.isoformat()[:-4] + 'Z'


def get_time_from_str(str_time):
    return datetime.fromisoformat(str_time[:-1] + '0000')
