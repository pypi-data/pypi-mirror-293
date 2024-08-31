import asyncio
from abstract_apis import get_url,make_endpoint
def getSolcatcherUrl():
  return 'https://solcatcher.io'
def getEndpointUrl(endpoint=None,url=None):
  url = url or getSolcatcherUrl()
  endpoint = make_endpoint(endpoint or '/')
  return get_url(url,endpoint)
def updateData(data,**kwargs):
  data.update(kwargs)
  return data
def getCallArgs(endpoint):
  return {'getMetaData': ['signature'], 'getPoolData': ['signature'], 'getTransactionData': ['signature'], 'getPoolInfo': ['signature'], 'getMarketInfo': ['signature'], 'getKeyInfo': ['signature'], 'getLpKeys': ['signature'], 'process': ['signature']}.get(get_endpoint(endpoint))
def ifListGetSection(listObj,section=0):
    if isinstance(listObj,list):
        if len(listObj)>section:
            return listObj[section]
    return listObj
def get_async_response(func, *args, **kwargs):
    if asyncio.get_event_loop().is_running():
        # If already inside an event loop, use ensure_future or create_task
        return asyncio.ensure_future(func(*args, **kwargs))
    else:
        return asyncio.run(func(*args, **kwargs))
