from TwitterAPI import TwitterAPI

SEARCH_TERM = ''
PRODUCT = 'fullarchive'
LABEL = 'SMI_tool'
SANDBOX_CONSUMER_KEY = 'd51IGnDlp7Aw58l4SnDufKop2'
SANDBOX_CONSUMER_SECRET = '92rDpKfnLUR01y69gU7KFo5iCWCIVBZgLOCtxerfNq6dhfO8vZ'
SANDBOX_TOKEN_KEY = '705985483-XBPCazD0DB1I9gh9SepR1S26FnTTubMsPONEttr9 '
SANDBOX_TOKEN_SECRECT = 'wPSaAbogn7kIgzOLm2EeMdtY0vZthDcrGHCBTDFe38RZ0'

api = TwitterAPI(SANDBOX_CONSUMER_KEY,
                 SANDBOX_CONSUMER_SECRET,
                 SANDBOX_TOKEN_KEY,
                 SANDBOX_TOKEN_SECRECT)

r = api.request('tweets/search/%s/:%s' % (PRODUCT, LABEL),
                {'query': SEARCH_TERM})

for item in r:
     print(item['text'] if 'text' in item else item)