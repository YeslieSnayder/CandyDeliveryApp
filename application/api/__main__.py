from application.api.__init__ import *
from application.api.handlers.post_couriers import *
from application.api.handlers.patch_courier import *
from application.api.handlers.get_courier import *
from application.api.handlers.post_orders import *
from application.api.handlers.assign_orders import *
from application.api.handlers.complete_order import *


if __name__ == '__main__':
    app.run(host=HOST, port=PORT)
