
import dns.resolver

def get_cname(domain):
    try:
        answers = dns.resolver.resolve(domain, 'CNAME')
        for rdata in answers:
            print('CNAME:', rdata.target.to_text())
    except Exception as e:
        print('Error:', e)

# Example usage
get_cname('smaht-productionblue-2001144827.us-east-1.elb.amazonaws.com')
