from api.__init__ import *
from api.handlers.post_couriers import *
from api.handlers.patch_courier import *
from api.handlers.get_courier import *
from api.handlers.post_orders import *
from api.handlers.assign_orders import *
from api.handlers.complete_order import *


if __name__ == '__main__':
    app.run(host=HOST, port=PORT)
