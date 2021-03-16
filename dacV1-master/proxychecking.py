import aiohttp
import asyncio
from aiohttp_socks import ProxyType, ProxyConnector, ChainProxyConnector
import sys

import nest_asyncio
nest_asyncio.apply()
# __import__('IPython').embed()


timeout = aiohttp.ClientTimeout(total=5)
payload = {'authorization': 'test'}

class ProxyChecker():
    def __init__ (self, proxyType, proxyList=[]):
        self.proxyType = proxyType
        self.proxyList = proxyList
        self.loop = asyncio.get_event_loop()


    async def begin_checking(self):
        tasks = (self.check_proxy(proxy, self.proxyType, self.proxyList.index(proxy)) for proxy in self.proxyList)
        self.loop.run_until_complete(asyncio.gather(*tasks))


        #tasks = (self.loop.run_until_complete(self.__async__check_proxy(proxy, self.proxyType)) for proxy in self.proxyList)
        #return asyncio.gather(*tasks, return_exceptions=True)


    def load_proxies(self):
        with open("config/proxies.txt", "r") as fd:
            for line in fd.readlines():
                line = line.strip("\n")
                if not line:
                    continue
                self.proxyList.append(line)


    def proxy_cleaner(self, del_proxylist):
        print("Deleting " + str(del_proxylist))
        with open("config/proxies.txt", "r") as f:
            lines = f.readlines()
        with open("config/proxies.txt", "w") as output:
            for line in lines:
                proxy = line.strip("\n")
                if not proxy:
                    continue
                if proxy not in del_proxylist:
                    output.write(line)
        for proxy in self.proxies:
            if proxy in del_proxylist:
                self.proxies.remove(proxy)
        

    async def check_proxy(self, proxy, proxyType, i):
        print(i)
        connector = ProxyConnector.from_url("{}://{}".format(proxyType, proxy))
        async with aiohttp.ClientSession(connector=connector, timeout=timeout) as session:
            responseJSON=""
            try:
                async with session.post('https://discord.com/api/v8/register', json=payload) as response:
                    while True:
                        status_code = response.status
                        try:
                            responseJSONpart = await response.read()
                        except asyncio.exceptions.IncompleteReadError as e:
                            responseJSON = responseJSON + e.partial.decode('utf-8')
                            continue
                        else:
                            responseJSON = responseJSON + responseJSONpart.decode('utf-8')
                            print(response.status)
                            break
                        
                        print(response.status)
                        break
            except Exception as e:
                result = get_full_class_name(e)
                if result == "proxy_socks._errors.ProxyConnectionError":
                    print("Failed proxy: {}".format(proxy))
                elif result == "asyncio.exceptions.TimeoutError":
                    print("timed out. #{}".format(i))


def get_full_class_name(obj):
    module = obj.__class__.__module__
    if module is None or module == str.__class__.__module__:
        return obj.__class__.__name__
    return module + '.' + obj.__class__.__name__


pc = ProxyChecker("socks4")
pc.load_proxies()
asyncio.run(pc.begin_checking())