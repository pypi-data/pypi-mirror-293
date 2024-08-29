
import urllib.parse
import json


class RequestParameters:
    def __init__(self,token:str,url:str|None=None, params:dict=None,proxy_mode:bool=False) -> None:
        self.apiurl = "api.scrape.do"
        self.proxyurl = "proxy.scrape.do:8080"
        self.token = token
        self.url = url
        self.params = {k.lower(): v for k, v in params.items()} if params else {}
        self.proxy_mode = proxy_mode
        assert self.token is not None and self.token != "", 'Scrape.do token is required'
        


    def encode(self) -> str:
        if "playwithbrowser" in self.params and isinstance(self.params["playwithbrowser"],list):
            self.params["playwithbrowser"] = json.dumps(self.params["playwithbrowser"],indent="")
        
        if "url" not in self.params:
            # that means if params has url, it will use that one.
            self.params["url"] = self.url
        
        encoded_params = '&'.join(f'{urllib.parse.quote(str(k))}={urllib.parse.quote(str(v),safe="")}' for k, v in self.params.items())
        return f'https://{self.apiurl}/?token={self.token}&{encoded_params}'
    
    def proxy(self) -> str:
        encoded_params = '&'.join(f'{urllib.parse.quote(str(k))}={urllib.parse.quote(str(v),safe="")}' for k, v in self.params.items() if k != "url")
        return "http://"+self.token+":"+encoded_params+"@"+self.proxyurl


    def copy(self) -> 'RequestParameters':
        return RequestParameters(
            token=self.token,
            url=self.url,
            params=self.params.copy()
        )


if __name__ == "__main__":
    # small unit test
    params = RequestParameters(
        url="https://httpbin.co/",
        token="TOKEN",
        params={
            "geoCode":"us",
            "sessionid":"123",
            "super":True,
            "render":True,
        },
    )

    print("api format: ",params.encode())
    print("proxy format: ",params.proxy())

        

