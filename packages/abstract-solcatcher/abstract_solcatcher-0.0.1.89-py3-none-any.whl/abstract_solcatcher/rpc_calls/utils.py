import asyncio
from ..utils import get_async_response
# Asynchronous version of makeParams
async def async_makeParams(*args, **kwargs):
    args = list(args)
    args.append({k: v for k, v in kwargs.items() if v is not None})
    return args

# Synchronous wrapper for makeParams
def makeParams(*args, **kwargs):
    return get_async_response(async_makeParams, *args, **kwargs)
