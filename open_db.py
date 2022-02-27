import shodan


def main():
    api_key = "D3JstZRg8nGXXZ2airRQ0MLMnjjUJJv5"

    api = shodan.Shodan(api_key)
    hosts = []
    while True:
        try:
            for banner in api.search_cursor('Russia'):
                hosts.append(banner["ip_str"])
        except Exception:
            break
    
    api = shodan.Shodan("FQNAMUdkeqXqVOdXsTLYeatFSpZSktdb")

    for host in hosts:
        host_obj = api.host(host)
        vulns = host_obj.get('vulns')
        print(f"Vulns {host}: {vulns}")
        # Write vulnerabilities to file
        if vulns:
            write_vulns(host, vulns)
        

def write_vulns(host, vulns, file="vulns.txt"):
    with open(file, "a+") as f:
        f.write(f"Host: {host}: {str(vulns)}\n")

if __name__ == "__main__":
    main()
