from ..abstract_rate_limit import makeLimitedCall
from .utils import makeParams, get_async_response
async def async_getLatestBlockHash(commitment=None):
    commitment = commitment or "processed"
    method = "getLatestBlockhash"
    params = await makeParams(commitment=commitment)
    return await makeLimitedCall(method, params)

def getLatestBlockHash(commitment=None):
    return get_async_response(async_getLatestBlockHash, commitment)

async def async_getSignaturesForAddress(address, limit=1000, before=None, after=None, finalized=None,encoding='jsonParsed',commitment=0,errorProof=False):
    finalized = finalized or True
    method = "getSignaturesForAddress"
    params = makeParams(address, limit=limit, before=before, after=after, finalized=finalized,encoding=encoding,commitment=commitment)
    signatureArray = await await makeLimitedCall(method, params)
    if errorProof:
        signatureArray = [signatureData for signatureData in signatureArray if signatureData.get('err') == None]
    return signatureArray

def getSignaturesForAddress(address, limit=1000, before=None, after=None, finalized=None,encoding='jsonParsed',commitment=0,errorProof=False):
    return get_async_response(async_getSignaturesForAddress, limit=limit, before=before, after=after, finalized=finalized,encoding=encoding,commitment=commitment,errorProof=errorProof)

async def async_getTransaction(signature,maxSupportedTransactionVersion=None):
    maxSupportedTransactionVersion=maxSupportedTransactionVersion or 0
    method = "getTransaction"
    params = makeParams(signature, maxSupportedTransactionVersion=maxSupportedTransactionVersion)
    return await await makeLimitedCall(method, params)

def getTransaction(signature,maxSupportedTransactionVersion=None):
    return get_async_response(async_getTransaction, signature,maxSupportedTransactionVersion=maxSupportedTransactionVersion)

async def async_getAccountInfo(account,encoding=None,commitment=None):
    encoding = encoding or "jsonParsed"
    commitment = commitment or 0
    method = "getAccountInfo"
    params = makeParams(account, encoding=encoding,commitment=commitment)
    return await await makeLimitedCall(method, params)

def getAccountInfo(account,encoding=None,commitment=None):
    return get_async_response(async_getAccountInfo, account,encoding=encoding,commitment=commitment)

async def async_getTokenAccountBalance(account,commitment=0):
    method = "getTokenAccountBalance"
    params = makeParams(account, commitment=commitment)
    return await makeLimitedCall(method, params)

def getTokenAccountBalance(account,commitment=0):
    return get_async_response(async_getTokenAccountBalance, account,commitment=commitment)

async def async_getTokenAccountByOwner(account,mint=None,encoding=None):
    encoding = encoding or "jsonParsed"
    method = "getTokenAccountByOwner"
    params = makeParams(account, mint=mint,encoding=encoding)
    return await makeLimitedCall(method, params)

def getTokenAccountByOwner(account,mint=None,encoding=None):
    return get_async_response(async_getTokenAccountByOwner, account,mint=mint,encoding=encoding)

async def async_sendTransaction(txn, skipPreflight=None, preflightCommitment=None):
    skipPreflight = skipPreflight or opts.skip_preflight
    preflightCommitment = preflightCommitment or "finalized"
    method = "sendTransaction"
    params = makeParams(txn, skipPreflight=skipPreflight, preflightCommitment=preflightCommitment)
    return await makeLimitedCall(method, params)

def sendTransaction(txn, skipPreflight=None, preflightCommitment=None):
    return get_async_response(async_sendTransaction, txn, skipPreflight=skipPreflight, preflightCommitment=preflightCommitment)


