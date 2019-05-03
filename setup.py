try:
	from config.config import __prefix__, __token__
	print('Import prefix and token from config, sucess')
except ImportError:
	print('Import prefix and token error')
	__prefix__ = '!'
	__token__ = 'NDA4NjU2ODk2NDk3NTQ5MzEy.DVTO7w.3SKVdlK6_1OLI8Jx0u7-UHIGpFY'