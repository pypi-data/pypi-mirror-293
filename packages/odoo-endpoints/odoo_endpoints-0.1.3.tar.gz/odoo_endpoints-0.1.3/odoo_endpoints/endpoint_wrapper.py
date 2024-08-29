
import logging 
from exceptions.api_exception import ApiException
import traceback

_logger = logging.getLogger(__name__)
class AppController():

	def dzexpert_api_endpoint(function):
		def wrapper(*args, **kwargs):
			try:
				result=function(*args, **kwargs)
				return {'status_code':200,'error':False,'result':result}
			except ApiException as ex:
				tb = traceback.format_exc()
				_logger.error(str(tb)) 
				_logger.debug("_____ error in  %s : "%(function)+str(ex.__str__())+"\n\n")
				return {'status_code':ex.http_code,'error':ex.message,'result':False}

		return wrapper