from datetime import datetime
from constant import timer as con_timer
from web_connection.req import get_new_tr_obj

def get_request_object(obj):
	obj_now = datetime.now()
	if obj_now.minute % con_timer.FOR_EVERY_X_MINUTE == 0:
		return get_new_tr_obj()
	else:
		return obj