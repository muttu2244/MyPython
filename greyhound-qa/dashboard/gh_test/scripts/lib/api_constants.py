import yaml
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__))+"/../config/")
class Constants(object):
	VERSION			= 'version'
	RESULT			= 'result'
	STATUS			= 'status'
	PARTIAL			= 'partial'
	ERROR			= 'error'
	MESSAGE			= 'message'
	#GRAPH_TYPE		= 'graph-type'
	GRAPH_TYPE_LIST		= 'graph-type-list'
	ZID_LIST		= 'uid-list'
	FILTER_CLAUSE		= 'filter-clause'
	META_FIELDS		= 'meta-fields'
	COLUMNS			= 'columns'
	DATA			= 'data'
	STMT			= 'stmt'
	FIELDS			= 'fields'
	ERROR_MSG_SUCCESS	= 'success'
	ERROR_CODE_SUCCESS	= 0
	BLOB			= 'blob'
	DELTA_STATUS		= 'deleted'
	CAS			= 'cas'
	GRAPH_LIST		= 'graph-list'
	CRED			= 'credibility'
	PREV_META_UPDATED	= 'prev-meta-updated'
	CREATE_USER		= 'create-if-not-exists'
	META_TYPE		= 'type'
	META_TYPE_GOLDEN	= 'golden'
	META_TYPE_CURRENT	= 'current'
	META_TYPE_PREVIOUS	= 'previous'
	COLUMN_COUNT		= 'column-count'
	
	HEADER_ZID		= 'X-ZID'
	HEADER_ZID_KEY		= 'HTTP_X_ZID'
	HEADER_ACCESS_ROLE	= 'X-Meta-Access-Role'
	HEADER_ACCESS_ROLE_KEY	= 'HTTP_X_META_ACCESS_ROLE'
	HEADER_ZAUTH		= 'Z-Authorization'
	HEADER_ZAUTH_KEY	= 'HTTP_Z_AUTHORIZATION'
	HTTP_X_REFERER		= 'X-Referer'
	HTTP_X_REFERER_KEY	= 'HTTP_X_REFERER'
	HTTP_IF_MATCH		= 'HTTP_IF_MATCH'
	HEADER_X_OPERATION	= 'X-Operation'
	HEADER_X_OPERATION_KEY	= 'HTTP_X_OPERATION'
	"""
	Various http header fields:
	HEADER_ZID - User ZID
	HEADER_ACCESS_ROLE - Access role (server or client)
	HEADER_ZAUTH - Auth token sent from client
	"""

	# Possible status values
	STATUS_SUCCESS		= True
	STATUS_FAILED		= False

	HTTP_RESULT_200		= '200 OK'
	HTTP_RESULT_400		= '400 Bad Request'
	HTTP_RESULT_401		= '401 Unauthorized'
	HTTP_RESULT_403		= '403 Forbidden'
	HTTP_RESULT_404		= '404 Not Found'
	HTTP_RESULT_444		= '444 No response'
	HTTP_RESULT_500		= '500 Internal server error'
	CONTENT_TYPE_JSON	= 'application/json'
	CONTENT_TYPE_BYTE_ARRAY	= 'application/octet-stream'
	CONTENT_TYPE_TEXT	= 'text/plain'

	# Type of params
	PARAM_REQUIRED		= 0x0001
	PARAM_OPTIONAL		= 0x0002
	PARAM_TYPE_INT		= 0x0004
	PARAM_TYPE_SCALAR	= 0x0008
	PARAM_TYPE_DICT		= 0x0010
	PARAM_TYPE_ARRAY	= 0x0020
	PARAM_TYPE_STRING	= 0x0040
	PARAM_TYPE_BOOL		= 0x0080
	"""
	Various flags used for parameter checking
	"""

	# Graph blob members
	GRAPH_VERSION		= "version"
	GRAPH_GRAPHS		= "graphs"
	GRAPH_CURR_VERSION	= 1
	"""
	GRAPH_VERSION -
	GRAPH_GRAPHS  -
	GRAPH_CURR_VERSION -
	"""

	# Graph sub-types
	GRAPH_MEMBERS		= "members"
	GRAPH_WAIT		= "wait"
	GRAPH_CONFIRM		= "confirm"
	"""
	Sub-lists within a graph object for a user
	GRAPH_MEMBERS -- list of users in the graph for the user
	GRAPH_WAIT -- list of users from which the user is awaiting response for friend request
	GRAPH_CONFIRM -- list of users who are awaiting response for friend request from the user
	"""

	# Some of the fixed meta fields
	META_FIELD_ZID		= 'zid'
	META_FIELD_MTIME	= 'mtime'
	META_FIELD_CRED		= 'cred'
	META_FIELD_CAS		= 'cas'
	META_FIELD_FLAGS	= 'flags'

	# CAS value provided for rows not existing in DB
	DEFAULT_CAS		= '00000000-0000-0000-0000-000000000000'

	# Roles
	ROLE_SERVER		= 'server'
	ROLE_CLIENT		= 'client'
	"""
	Supported roles
	- ROLE_SERVER -- Zynga internal servers
	- ROLE_CLIENT -- External game clients
	"""

	# Meta field scope
	META_SCOPE_NONE		= 'none'
	META_SCOPE_SELF		= 'self'
	META_SCOPE_ALL		= 'all'
	"""
	The visibility scope of meta fields in DB
	- META_SCOPE_NONE -- The meta field is viewable only by admin apis
	- META_SCOPE_SELF -- The meta field is viewable/editable by the user
	- META_SCOPE_ALL -- The meta field is viewable by user's friends
	"""

	# DB types supported
	DB_TYPE_INT		= 'integer'
	DB_TYPE_UINT		= 'unsigned integer'
	DB_TYPE_DATETIME	= 'datetime'
	DB_TYPE_VARCHAR		= 'varchar'
	DB_TYPE_REAL		= 'real'
	"""
	Type of meta fields currently supported
	DB_TYPE_INT	- signed integer (64-bit)
	DB_TYPE_UINT	- unsigned integer (64-bit)
	DB_TYPE_DATETIME - date time
	DB_TYPE_VARCHAR	- varchar. Size is required for varchar fields.
	DB_TYPE_REAL	- double 
	"""

	DB_VARCHAR_LIMIT	= 255
	"""
	Maximum varchar meta fields supported in MQS
	"""

	SECONDS_IN_DAY		= (24 * 60 * 60)

	# Params used in apis to populate DB
	START			= 'start'
	END			= 'end'
	COUNT			= 'count'
	SCHEMA			= 'schema'
	X			= 'x'
	Y			= 'y'
	X_LIMIT			= 'x_limit'
	OFFSET			= 'offset'
	X_OFFSET		= 'x-offset'
	Y_OFFSET		= 'y-offset'

	# Dev flags
	DISABLE_CAS_CHECK	= 'disable_cas_check'
	CONVERT_API_ERR_TO_HTTP_ERR = 'convert_api_err_to_http_err'
	GEN_RANDOM_CAS_ERROR	= 'gen_random_cas_error'
	"""
	Developer flags
	- DISABLE_CAS_CHECK - Disables cas while meta updates
	- CONVERT_API_ERR_TO_HTTP_ERR - Converts API error to HTTP error
	- GEN_RANDOM_CAS_ERROR - Simulate cas error in graph membase API
	"""

	API_MAP_SIZE		= 5
	"""
	Size of the api_map structure
	It contains the following elements:
		- name of api
		- api handler
		- supported roles
		- input headers
		- input params
	"""

	# gh web server supported 
	BLOBS			= 'blobs'
	GH_CAS			= 'CAS'
	GH_HEADER		= 'header'
	GH_MD5			= 'md5'
	GH_MTIME		= 'mtime'
	GH_BLOB			= 'blob64'
	GH_ERROR		= 'error'
	GH_CTIME		= 'time'
	GH_ERROR_MESSAGE	= 'errorMessage'
	GH_BLOB64		= 'blob64'
	USER_QUERY		= 'query'
	USER_PARAMS		= 'params'
	DELTA_TYPE		= 'type'
	#DELTA_STATUS		= 'status'
	"""
	Other constants used in storage services read from the yaml config file
	"""
	f = open(os.path.dirname(os.path.abspath(__file__))+"/../config/load_config.yaml")
	config = yaml.load(f.read())
	
	SERVICE_URLS 		= config["storage"]['url']
	SERVICE_URL 		= SERVICE_URLS.split(',')
	SECRET 			= config['storage']['secret']
	XREFERER 		= config['storage']['xreferer']
	USER_BLOB 		= config['storage']['blob_type']
	USER_BLOB2		= config['storage']['blob_type2']
	DELTATYPE 		= config['storage']['delta_type']
	XOR_ENCODE 		= config['storage']['xor_encode']
	DISABLE_AUTH 		= config['storage']['disable_auth']
	ZID 			= config['storage']['zid']	
	NZID			= config['storage']['nzid']
	INVALID_DELTA 		= config['storage']['invalid_delta']
	INVALID_BLOB 		= config['storage']['invalid_blob']
	EMPTY_BLOB 		= config['storage']['empty_blob']
	MULTI_TENDENCY 		= config['storage']['multi_tendency']
	GAME_ID 		= config['storage']['game_id']
	SELF_QUERY 		= config['storage']['user_query']
	F_QUERY 		= config['storage']['friend_query']
	INVALID_DELTAID		= config['storage']['invalid_deltaID']
	APP_NAMESPACE           = config['storage']['app_namespace']
	SCOREBOARD_TYPE         = config['storage']['scoreboard_type']
	MQS_URLS		= config["mqs"]['url']
	MQS_URL			= MQS_URLS.split(',')	
	GRAPH_TYPE		= config['mqs']['graph_type']
	INTERNAL_URLS		= config["internal"]['url']
	INTERNAL_URL		= INTERNAL_URLS.split(',')
	#GAME_ID			= config['internal']['game_id']
	VERSION			= config['internal']['version']
	GH_MEMSCHED		= config['internal']['gh_memsched']
	PORT			= config['internal']['port']
	LEVEL			= config['internal']['level']
	ARCHIVE_INTERVAL	= config ['internal']['archive_interval']
	ADMIN_URLS		= config['admin']['url']
        ADMIN_URL               = ADMIN_URLS.split(',')
	
	
	
	
		
