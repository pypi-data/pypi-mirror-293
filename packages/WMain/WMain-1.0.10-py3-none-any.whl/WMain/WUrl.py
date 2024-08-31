"""
class: WUrl


"""
from typing import List, Dict, Union    
import urllib.parse

class WUrlFormatException(Exception):
    pass

class WUrl:
    
    __attr__ = [
        "protocol",             # http, https, ftp, ftps, file, etc.
        "host_domain_port",     # www.example.com:8080
        "path_str", 
        "path",                 # /path/to/file.html    
        "params_str",
        "params",               # ?key1=value1&key2=value2
        "fragment"              # #section1
    ]
    protocol: str = ""   
    host_domain_port: str = ""
    _path_str: str = ""
    path: List[str] = []
    _params_str: str = ""
    params: Dict[str, str] = {}
    fragment: str = ""
    
    def __init__(self, url: str) -> None:
        if isinstance(url, WUrl):
            url = url.__str__()
        self.parse_url(url)
        
    def parse_url(self, url: str) -> None:
        url = urllib.parse.unquote(url)
        if url.find("://") == -1:
            raise WUrlFormatException("Invalid URL format: missing protocol")
        self.protocol, url = url.split("://" , 1)
        if url.find("/") == -1:
            self.host_domain_port = url
            self._path_str = ""
            self.path = []
            self._params_str = ""
            self.params = {}
            self.fragment = ""
            return
        if url.find("#") != -1:
            url, self.fragment = url.split("#", 1)
        if url.find("?") != -1:
            url, self._params_str = url.split("?", 1)
        self.host_domain_port, self._path_str = url.split("/", 1)
        self.params_str_to_params()
        self.path_str_to_path()
    
    def params_str_to_params(self):
        if not self._params_str:
            self._params_str = ""
            self.params = {}
            return
        self.params = {}
        for param in self._params_str.split("&"):
            if param.find("=") == -1:
                raise WUrlFormatException(f"Invalid URL format: missing value for parameter---{param}")
            key, value = param.split("=", 1)
            self.params[key] = value
    
    def path_str_to_path(self):
        if not self._path_str:
            self._path_str = ""
            self.path = []
            return
        self.path = self._path_str.split("/")
    
    def path_to_path_str(self):
        self._path_str = "/".join(self.path)
    
    def params_to_params_str(self):
        self._params_str = "&".join([f"{key}={value}" for key, value in self.params.items()])
    
    def __str__(self) -> str:
        url = f"{self.protocol}://{self.host_domain_port}"
        if self._path_str:
            url += f"/{self._path_str}"
        if self._params_str:
            url += f"?{self._params_str}"
        if self.fragment:
            url += f"#{self.fragment}"
        return url
        
    
    def __repr__(self) -> str:
        return self.__str__()
    
    def __getitem__(self, key: Union[str, int]) -> str:
        if isinstance(key, int):
            return self.path[key]
        else:
            return self.params[key]
    
    def __setitem__(self, key: Union[str, int], value) -> None:
        value = str(value)
        if isinstance(key, int):
            self.path[key] = value
            self.path_to_path_str()
        else:
            self.params[key] = value
            self.params_to_params_str()
        
    
    def __delitem__(self, key: Union[str, int]) -> None:
        if isinstance(key, int):
            del self.path[key]
        else:
            del self.params[key]
    
    def copy(self) -> "WUrl":
        return WUrl(self.__str__())
        
    
    def urljoin(self, part: str):
        """
        Returns:
            WUrl: _description_
        """
        if part.find("://") != -1:
            return WUrl(part)
        elif part.startswith("/"):
            return WUrl(f"{self.protocol}://{self.host_domain_port}{part}")
        else:
            return WUrl(f"{self.protocol}://{self.host_domain_port}/{'/'.join(self.path[:-1])}/{part}")
    
    def get_quoted_url(self) -> str:
        return urllib.parse.quote(self.__str__())
    
    def get_unquoted_url(self) -> str:
        return urllib.parse.unquote(self.__str__())

# TEST
if __name__ == "__main__":
    # 生成一个100字符以上的符合规范, 有所有的url关键点的url
    url = "https://www.example.com/products/electronics/television?brand=samsung&size=55inch&resolution=4k&color=black&priceRange=1000-1500&sortBy=price&discounted=true&source=affiliate&campaign=summer-sale-2022&utm_medium=email&utm_source=newsletter&tracking=123456#reviews"
    print(url)
    wurl = WUrl(url)
    print(wurl)
    url = "https://v11.tlkqc.com/wjv11/202403/10/3ECUvkBD6L3/video/index.m3u8?123=411"
    wurl = WUrl(url)
    wurl[1] = 111
    wurl["123"] = 123
    print(wurl)
    
    
    