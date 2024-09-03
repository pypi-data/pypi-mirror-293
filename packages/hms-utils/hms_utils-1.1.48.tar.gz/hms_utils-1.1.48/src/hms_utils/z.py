import requests
from urllib.parse import urlparse

def get_final_redirect_url(url):
    def get_domain_name(url):
        parsed_url = urlparse(url)
        domain = parsed_url.netloc.split(':')[0]  # Remove port if present
        return domain
    try:
        import pdb ; pdb.set_trace()  # noqa
        response = requests.get(url, allow_redirects=True)
        x = response.url
        y = response.headers
        print(x)
        print(y)
        return get_domain_name(x)
    except requests.RequestException as e:
        return f"Error: {e}"

# Example usage
original_url = "http://smaht-productionblue-2001144827.us-east-1.elb.amazonaws.com"
final_url = get_final_redirect_url(original_url)
print(f"The final URL is: {final_url}")
