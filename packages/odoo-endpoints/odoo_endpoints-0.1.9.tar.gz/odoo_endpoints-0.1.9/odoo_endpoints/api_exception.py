class ApiException(Exception):
	def __init__(self,http_code=500,custom_error='Unexpected Error',**data):
		self.http_code=http_code
		if http_code==500:
			self.message = 'Server Exception'
		elif http_code==409:
			self.message = 'Already Exists'
		elif http_code==403:
			self.message = 'Forbidden Access'
		elif http_code==401:
			self.message = 'Unauthorized'
		elif http_code==400:
			self.message = 'Bad Request'
		else:
			self.message=custom_error
		message=self.message         
		self.data=data
		super().__init__(message)
