import yaml
from api_constants import Constants
class ConfigService:
	@staticmethod
	def getConfig():
		path = "/apps/%s/current/Storage.yaml" % (Constants.GAME_ID)
		f = open(path)
		config = yaml.load(f.read())
		f.close()
		return config


	@staticmethod
	def getBlobTypesByNamespace(namespace):	
		config = ConfigService.getConfig()
		ns = config[namespace]
		types = []
		for d in ns:
			if d['type'] != '*':
				types.append( d['type'])
			
		return types

	@staticmethod
	def getGoldenBlobTypes():
		return ConfigService.getBlobTypesByNamespace('Golden')

	@staticmethod
	def getBlobTypes(golden = False):
		if(golden):
			return ConfigService.getGoldenBlobTypes()
		else:
			return ConfigService.getBlobTypesByNamespace('Blobs')

	@staticmethod
	def getDeltaTypes():
		return ConfigService.getBlobTypesByNamespace('Deltas')

	@staticmethod
	def getScoreboardTypes():
		return ConfigService.getBlobTypesByNamespace('Scoreboard')

	@staticmethod
	def getArchiveBlobTypes():
		return ConfigService.getBlobTypesByNamespace('Archive')

	@staticmethod
	def getGoldenBlobPool(blob_type):
		return ConfigService.getBlobPool(blob_type, True)


	@staticmethod
	def getBlobPool(blob_type, golden = False):
		config = ConfigService.getConfig()
		if golden:
			blobs = config['Golden']
		else:
			blobs = config['Blobs']
		
		wildcard = None

		for b in blobs:
			if b['type'] == '*':
				wildcard = b
			if b['type'] == blob_type:
				try:
					if b['pool'] is not None:
						return b['pool']
				except KeyError:
					if wildcard is not None:
						return wildcard['pool']

		return None

	@staticmethod
	def getDeltaPool(delta_type = None):
		config = ConfigService.getConfig()
		deltas = config['Deltas']
		wildcard = None

		for d in deltas:
			if d['type'] == '*':
				wildcard = d
				try:
					if delta_type is None and wildcard['pool'] is not None:
						return wildcard['pool']
				except KeyError:
					return None

			if d['type'] == delta_type:
				try: 
					if d['pool'] is not None:
						return d['pool']
				except KeyError:
					if wildcard is not None:
						return wildcard['pool']

		return None

	@staticmethod
	def parseSize(sz):
		suffix = sz[sz.__len__()-1]
		
		if suffix == 'k' or suffix == 'K':
			return int(sz[0:sz.__len__()-1]) * 1024
		elif suffix == 'm' or suffix == 'M':
			return int(sz[0:sz.__len__()-1]) * 1024 *1024

		return int(sz[0:sz.__len__()])

	
	@staticmethod
	def getBlobLimits(blob_type):
		config = ConfigService.getConfig()
		blobs = config['Blobs']
		wildcard = None
		
		for b in blobs:
			
			if b['type'] == '*':
				wildcard = b
			if b['type'] == blob_type:
				try:
					if b['maxsize'] is not None:
						maxsize = ConfigService.parseSize(b['maxsize'])
						return {'maxsize': maxsize}
				except KeyError:
					if wildcard['maxsize'] is not None:
						maxsize = ConfigService.parseSize(wildcard['maxsize'])
						return {'maxsize': maxsize}

		return None


	@staticmethod
	def getDeltaLimits(delta_type):
		config = ConfigService.getConfig()
		deltas = config['Deltas']
		wildcard = None

		maxcount = 0
		keep = True

		for d in deltas:
			
			if d['type'] == '*':
				wildcard = d
				try:
					wildcard['ttl']
					wildcard['maxcount']
				except KeyError:
					return None
			if d['type'] == delta_type:
				try:
					if d['ttl'] is not None:
						ttl = d['ttl']
				except KeyError:
					if wildcard['ttl'] is not None:
						ttl = wildcard['ttl']

				try:
					if d['maxsize'] is not None:
						maxsize = ConfigService.parseSize(d['maxsize'])
				except KeyError:
					if wildcard['maxsize'] is not None:
						maxsize = ConfigService.parseSize(wildcard['maxsize'])
				

				try:
					if d['maxcount'] is not None:
						maxcount = d['maxcount']
				except KeyError:
					if wildcard['maxcount'] is not None:
						maxcount = wildcard['maxcount']

				try:
					if d['keep'] is not None:
						keep = (d['keep'] == 'oldest')
				except KeyError:
					keep = (wildcard['keep'] == 'oldest')

				
				return {'maxsize': maxsize, 'maxcount': int(maxcount), 'ttl': int(ttl), 'keep': keep}

		return None



	@staticmethod
	def getScoreBoardLimits(type):
		config = ConfigService.getConfig()
		deltas = config['Scoreboard']
		wildcard = None

		maxcount = 0
		keep = True

		for d in deltas:
		
			if d['type'] == '*':
				wildcard = d
				try:
					wildcard['ttl']
					wildcard['min']
					wildcard['max']
				except KeyError:
					return None

			if d['type'] == type:
				try:
					if d['ttl'] is not None:
						ttl = d['ttl']
				except KeyError:
					if wildcard['ttl'] is not None:
						ttl = wildcard['ttl']

				try:
					if d['max'] is not None:
						max = d['max']
				except KeyError:
					if wildcard['max'] is not None:
						max = wildcard['max']
				
				try:
					if d['min'] is not None:
						min = d['min']
				except KeyError:
					if wildcard['min'] is not None:
						min = wildcard['min']

				try:
					if d['maxcount'] is not None:
						maxcount = d['maxcount']
				except KeyError:
					if wildcard['maxcount'] is not None:
						maxcount = wildcard['maxcount']

				return {'max': int(max), 'min': int(min), 'ttl': int(ttl), 'maxcount': int(maxcount)}

		return None



