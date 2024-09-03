aname = "smaht-productionblue-2001144827.us-east-1.elb.amazonaws.com"
import dns.resolver

def get_cname_records(domain):
    try:
        # Query the CNAME records
        answers = dns.resolver.resolve(domain, 'CNAME')
        for rdata in answers:
            print(f'CNAME Record: {rdata.target}')
    except dns.resolver.NoAnswer:
        print('No CNAME record found.')
    except dns.resolver.NXDOMAIN:
        print('Domain does not exist.')

# Example usage
get_cname_records('staging.smaht.org')
