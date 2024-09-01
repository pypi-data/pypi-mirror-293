from ..utils import get_async_response,getEndpointUrl,get_headers
from ..async_utils import asyncPostRequest
import json,requests

async def get_solcatcher_endpoint(endpoint,*args,**kwargs):
    return requests.post(url=getEndpointUrl(endpoint),data=json.dumps(kwargs),headers=get_headers())
  
def getTxnTypeFromMint(address):
    return get_async_response(get_solcatcher_endpoint,endpoint="getTxnTypeFromMint",address=address)

def sendTransaction(txn, skipPreflight=None, preflightCommitment=None):
  return get_async_response(get_solcatcher_endpoint,endpoint="sendTransaction",txn=txn, skipPreflight=skipPreflight, preflightCommitment=preflightCommitment)


def getGenesisSignature(address,before=None,limit=None):
  return get_async_response(get_solcatcher_endpoint,endpoint="getGenesisSignature",address=address,before=before,limit=limit)

def getSignaturesForAddress(address, limit=10, before=None, after=None, finalized=None,encoding=None,commitment=None,errorProof=False):
  return get_async_response(get_solcatcher_endpoint,endpoint="getSignaturesForAddress",address=address, limit=limit, before=before, after=after, finalized=finalized,encoding=encoding,commitment=commitment,errorProof=errorProof)

def getTokenAccountBalance(account,mint=None,commitment=None):
  return get_async_response(get_solcatcher_endpoint,endpoint="getTokenAccountBalance",account=account,mint=mint,commitment=commitment)

def getTokenAccountsByOwner(account,mint=None,encoding=None):
  return get_async_response(get_solcatcher_endpoint,endpoint="getTokenAccountsByOwner",account=account,mint=mint,encoding=encoding)

def getMetaData(address):
  return get_async_response(get_solcatcher_endpoint,endpoint="getMetaData",address=address)

def getTransaction(signature,maxSupportedTransactionVersion=None):
  return get_async_response(get_solcatcher_endpoint,endpoint="getTransaction",signature=signature,maxSupportedTransactionVersion=maxSupportedTransactionVersion)

def getLatestBlockHash(commitment=None):
    return get_async_response(get_solcatcher_endpoint,endpoint="getLatestBlockhash",commitment=commitment)

def getAccountInfo(account,encoding=None,commitment=None):
  return get_async_response(get_solcatcher_endpoint,endpoint="getAccountInfo",account=account,encoding=encoding,commitment=commitment)

def getBlock(slot,encoding=None,maxSupportedTransactionVersion=None,transactionDetails= None,rewards=None):
    return get_async_response(get_solcatcher_endpoint,endpoint="getBlock",slot=slot,encoding=encoding,maxSupportedTransactionVersion=maxSupportedTransactionVersion,transactionDetails=transactionDetails,rewards=rewards)


