from .url_model import URL
from django.db.models import F
import re

WEB_LINK = "https://turl.com/redirect/id?="

def valid_url(url):
    regex = re.compile(
        r'^(?:http|ftp)s?://' # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
        r'localhost|' #localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
        r'(?::\d+)?' # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    return re.match(regex, url)
    

def create_short_url(url):
    short_url = hash(url)
    URL.objects.create(long_url=url, short_url=short_url)
    return f"{WEB_LINK}{short_url}"

def get_short_url(url):
    return f"{WEB_LINK}{URL.objects.get(long_url=url).short_url}"


def check_if_long_url_exists(long_url) -> bool:
    return URL.objects.filter(long_url=long_url).exists()

def check_if_short_url_exists(short_url) -> bool:
    return URL.objects.filter(short_url=short_url).exists()
    
def url_shortner(url):
    if check_if_long_url_exists(url):
        return get_short_url(url)
    return create_short_url(url)
    
def get_long_url(url):
    return URL.objects.get(short_url=url).long_url

def increment_visits(short_url):
    return URL.objects.filter(short_url=short_url).update(visit_count=F('visit_count') + 1)

def get_short_url_stats(short_url):
    return URL.objects.get(short_url=short_url).visit_count