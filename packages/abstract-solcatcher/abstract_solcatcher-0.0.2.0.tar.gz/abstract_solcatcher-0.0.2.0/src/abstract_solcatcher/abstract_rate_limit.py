from .utils import getEndpointUrl,get_async_response
from abstract_apis import get_headers,requests,asyncPostRpcRequest,asyncPostRequest,asyncGetRequest
import json
async def asyncMakeLimitedDbCall(method=None, params=[]):
    checkSolcatcherDbUrl = getEndpointUrl("dbSearch")
    response = requests.get(url=checkSolcatcherDbUrl, data=json.dumps({"method":method, "params":params}),headers=get_headers())
    if response.json().get('result') != None:
      print('search successful')
      return response.json().get('result')
    urls = await async_get_rate_limit_url(method)
    response = await asyncPostRpcRequest(
        url=urls.get('url'), method=method, params=params, status_code=True, response_result='result'
    )
    
    if response[1] == 429:
        response = await asyncPostRpcRequest(
            url=urls.get('url2'), method=method, params=params, response_result='result', status_code=True
        )
    await async_log_response(method, response[0])
    insertSolcatcherDbUrl = getEndpointUrl("dbInsert")
    await asyncPostRequest(url=insertSolcatcherDbUrl, data={"method":method, "params":params,"result":response[0]}, status_code=True)
    return response[0]

def makeLimitedDbCall(method=None, params=[]):
    return get_async_response(asyncMakeLimitedDbCall, method, params)

async def asyncMakeLimitedCall(method=None, params=[]):
    urls = await async_get_rate_limit_url(method)
    response = await asyncPostRpcRequest(
        url=urls.get('url'), method=method, params=params, status_code=True, response_result='result'
    )
    
    if response[1] == 429:
        response = await asyncPostRpcRequest(
            url=urls.get('url2'), method=method, params=params, response_result='result', status_code=True
        )
    
    await async_log_response(method, response[0])
    return response[0]

def makeLimitedCall(method=None, params=[]):
    return get_async_response(asyncMakeLimitedCall, method, params)

async def async_get_rate_limit_url(method='default_method'):
    return await asyncGetRequest(url=getEndpointUrl("rate_limit"),data={"method":str(method)})

def get_rate_limit_url(method_name, *args, **kwargs):
    return get_async_response(async_get_rate_limit_url, method_name, *args, **kwargs)

async def async_log_response(method='default_method', response_data={}):
    return await asyncPostRequest(url=getEndpointUrl("log_response"),data={"method":str(method),"response_data":response_data})

def log_response(method_name, response_data, *args, **kwargs):
    return get_async_response(async_log_response, method_name, response_data, *args, **kwargs)
