
import logging 
from . import api_exception
import traceback

_logger = logging.getLogger(__name__)
def api_endpoint(function):
	def wrapper(*args, **kwargs):
		try:
			result=function(*args, **kwargs)
			return {'status_code':200,'error':False,'result':result}
		except api_exception.ApiException as ex:
			tb = traceback.format_exc()
			_logger.error(str(tb)) 
			_logger.debug("_____ error while calling  %s : "%(function)+str(ex.__str__())+"\n\n")
			return {'status_code':ex.http_code,'error':ex.message,'result':False,**ex.data}
		except Exception as ex:
			tb = traceback.format_exc()
			_logger.error(str(tb)) 
			_logger.debug("_____ error while calling  %s : "%(function)+str(ex.__str__())+"\n\n")
			return {'status_code':500,'error':ex.__str__(),'result':False}

	return wrapper