import json
import urllib3

class ProxyLib(object):

    http = urllib3.PoolManager()
    url: str = ''
    
    async def make_request(config, payload):
        try:
            response = ProxyLib.http.request(
                config['method'], 
                f"{ProxyLib.url}/{config['url']}", 
                body = json.dumps(payload).encode('utf-8'),
                headers = config['headers']
            )
            resp = json.loads(response.data.decode('utf-8'))
            if 'message' not in resp:
                raise Exception(resp['detail' if 'detail' in resp else 'error' if 'error' in resp else 'body'])

            return resp['message']
        except Exception as e:
            print(e)
            return {
                "error": str(e)
            }