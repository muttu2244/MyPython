from api_constants import Constants

class ApiError(object):
	ENOINPUTPARAMETER	= 1
	ENOINPUTHEADERFIELD	= 2
	EVERSIONNOTSUPPORTED	= 3
	EQUERYPARSEFAILED	= 4
	EINTERNALERROR		= 5
	EINTERNALAPIERROR	= 6
	ECONNECTIONERROR	= 7
	EINVALIDINPUT		= 8
	EDATABASEERROR		= 9
	EUNEXPECTEDINPUTPARAM	= 10
	EINPUTERROR		= 11
	ENODATA			= 12
	EBADDATA		= 13
	ESTALEDATA		= 14
	ERETRY			= 15

	@staticmethod
	def noInputParameter(input):
		return [ ApiError.ENOINPUTPARAMETER, "Required parameter '%s' not provided in input." % input ]

	@staticmethod
	def noInputHeaderField(input):
		return [ ApiError.ENOINPUTHEADERFIELD, "Header field '%s' not provided in input." % input ]

	@staticmethod
	def versionNotSupported(version, supported_version = None):
		err_msg = "Version %d is not supported. " % version
		if supported_version:
			err_msg += "The current supported version is %d. " % supported_version
		return [ ApiError.EVERSIONNOTSUPPORTED, err_msg ]

	@staticmethod
	def queryParseFailed(query):
		return [ ApiError.EQUERYPARSEFAILED, "Unable to parse query '%s'." % query ]

	@staticmethod
	def internalError(msg):
		return [ ApiError.EINTERNALERROR, msg ]

	@staticmethod
	def internalApiError(status):
		return [ status[Constants.ERROR], status[Constants.MESSAGE] ]

	@staticmethod
	def connectionError(msg):
		return [ ApiError.ECONNECTIONERROR, msg ]

	@staticmethod
	def invalidInput(msg):
		return [ ApiError.EINVALIDINPUT, msg ]

	@staticmethod
	def databaseError(msg):
		return [ ApiError.EDATABASEERROR, msg ]

	@staticmethod
	def unexpectedInputParam(param):
		err_msg = "Unexpected input param '%s' provided to api" % param
		return [ ApiError.EUNEXPECTEDINPUTPARAM, err_msg ]

	@staticmethod
	def inputError(api):
		err_msg = "Unable to parse input for %s api" % api
		return [ ApiError.EINPUTERROR, err_msg ]

	@staticmethod
	def noData(msg):
		return [ ApiError.ENODATA, msg ]

	@staticmethod
	def badData(msg):
		return [ ApiError.EBADDATA, msg ]

	@staticmethod
	def staleData(msg):
		return [ ApiError.ESTALEDATA, msg ]

	@staticmethod
	def retry(msg):
		return [ ApiError.ERETRY, "Retry the operation : %s" % (msg) ]

