from torrequest import TorRequest

def get_new_tr_obj():
	tr = TorRequest(proxy_port=9050, ctrl_port=9051, password='kktnvilm')
	return tr