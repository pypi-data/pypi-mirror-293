import dns.resolver

def get_cname_record(domain):
    try:
        answers = dns.resolver.resolve(domain, 'CNAME')
        return [str(answer.target) for answer in answers]
    except dns.resolver.NoAnswer:
        return None
    except dns.resolver.NXDOMAIN:
        return None

domain = "smaht-productionblue-2001144827.us-east-1.elb.amazonaws.com"
cname_records = get_cname_record(domain)
if cname_records:
    print(f"CNAME records for {domain}: {cname_records}")
else:
    print(f"No CNAME records found for {domain}.")
