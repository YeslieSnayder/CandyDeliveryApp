from model.exeptions import *


class TypeCourier:
    FOOT = {'name': 'foot', 'payload': 10}
    BIKE = {'name': 'bike', 'payload': 15}
    CAR = {'name': 'car', 'payload': 50}


class Courier:
    """
    Class represented couriers:
    courier_id ->    integer >= 1
    courier_type ->  type of the courier: {foot, bike, car}
    regions ->       the list of regions' id in which the courier works
    working_hours -> the list of working hours of the courier {HH:MM-HH:MM}
    """

    def __init__(self, obj):
        if len(obj) != 4 or obj['courier_id'] < 1 \
                or obj['courier_id'] is None \
                or obj['courier_type'] is None \
                or obj['regions'] is None \
                or obj['working_hours'] is None \
                or obj['courier_type'] != TypeCourier.FOOT['name'] \
                and obj['courier_type'] != TypeCourier.BIKE['name'] \
                and obj['courier_type'] != TypeCourier.CAR['name']:
            raise WrongCourierData([obj['courier_id']])
        self.courier_id = obj['courier_id']
        self.courier_type = obj['courier_type']
        self.regions = obj['regions']
        self.working_hours = obj['working_hours']


class Model:
    def __init__(self):
        self.couriers = []

    def add_courier(self, courier):
        c = Courier(courier)
        self.couriers.append(c)

    def create_couriers(self, couriers):
        wrong_ids = []
        correct_couriers = []
        for obj in couriers:
            try:
                correct_couriers.append(Courier(obj))
            except WrongCourierData as e:
                wrong_ids.append(e.args[0][0])
        if len(wrong_ids) != 0:
            raise WrongCourierData(wrong_ids)

        for courier in correct_couriers:
            self.couriers.append(courier)
        return [c.courier_id for c in correct_couriers]
