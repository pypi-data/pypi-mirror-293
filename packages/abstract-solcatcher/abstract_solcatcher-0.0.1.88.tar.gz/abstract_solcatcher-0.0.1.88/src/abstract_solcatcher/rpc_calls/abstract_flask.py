from ..abstract_rate_limit import makeLimitedCall
from .utils import makeParams, get_async_response
from solana.rpc.types import TokenAccountOpts,TxOpts
from solana.transaction import Transaction
import base58
async def async_getLatestBlockHash(commitment=None):
    commitment = commitment or "processed"
    method = "getLatestBlockhash"
    params = await makeParams(commitment=commitment)
    return await makeLimitedCall(method, params)

def getLatestBlockHash(commitment=None):
    return get_async_response(async_getLatestBlockHash, commitment)

async def async_getSignaturesForAddress(address, limit=None, before=None, after=None, finalized=None,encoding=None,commitment=None,errorProof=False):
    finalized = finalized or True
    method = "getSignaturesForAddress"
    params = makeParams(address, limit=limit or 1000, before=before, after=after, finalized=finalized,encoding=encoding or 'jsonParsed',commitment=commitment or 0)
    signatureArray = await makeLimitedCall(method, params)
    if errorProof:
        signatureArray = [signatureData for signatureData in signatureArray if signatureData.get('err') == None]
    return signatureArray

def getSignaturesForAddress(address, limit=None, before=None, after=None, finalized=None,encoding=None,commitment=None,errorProof=False):
    return get_async_response(async_getSignaturesForAddress, limit=limit, before=before, after=after, finalized=finalized,encoding=encoding,commitment=commitment,errorProof=errorProof)

async def async_getTransaction(signature,maxSupportedTransactionVersion=None):
    maxSupportedTransactionVersion=maxSupportedTransactionVersion or 0
    method = "getTransaction"
    params = makeParams(signature, maxSupportedTransactionVersion=maxSupportedTransactionVersion)
    return await makeLimitedCall(method, params)

def getTransaction(signature,maxSupportedTransactionVersion=None):
    return get_async_response(async_getTransaction, signature,maxSupportedTransactionVersion=maxSupportedTransactionVersion)

async def async_getAccountInfo(account,encoding=None,commitment=None):
    encoding = encoding or "jsonParsed"
    commitment = commitment or 0
    method = "getAccountInfo"
    params = makeParams(account, encoding=encoding,commitment=commitment)
    return await makeLimitedCall(method, params)

def getAccountInfo(account,encoding=None,commitment=None):
    return get_async_response(async_getAccountInfo, account,encoding=encoding,commitment=commitment)

async def async_getTokenAccountBalance(account,commitment=None):
    method = "getTokenAccountBalance"
    params = makeParams(account, commitment=commitment or 0)
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

async def async_sendTransaction(txn: Transaction, payer_keypair,skipPreflight=True, preflightCommitment=None):
    txn.sign(payer_keypair)
    txn_base58 = base58.b58encode(txn.serialize()).decode('utf-8')
    opts=TxOpts(skip_preflight=skipPreflight)
    preflightCommitment = preflightCommitment or "finalized"
    method = "sendTransaction"
    params = makeParams(txn_base58, skipPreflight=opts.skipPreflight, preflightCommitment=preflightCommitment)
    return await makeLimitedCall(method, params)

def sendTransaction(txn: Transaction, payer_keypair,skipPreflight=True, preflightCommitment=None):
    return get_async_response(async_sendTransaction, txn, payer_keypair=payer_keypair, skipPreflight=skipPreflight, preflightCommitment=preflightCommitment)


