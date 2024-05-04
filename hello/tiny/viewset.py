from hello.tiny.utils import (
    check_if_short_url_exists,
    get_long_url, 
    get_short_url_stats,
    increment_visits, 
    url_shortner, 
    valid_url
)
from django.http import Http404
from rest_framework.decorators import action
from logging import logger

@action(detail=False, methods=['post'], url_path='shorten')
def shorten(request):
    if not valid_url(request.data['url']):
        logger(f"Requested URL: {request.data['url']} is invalid")
        return Http404("Invalid URL")
    response = url_shortner(request.data['url']) 
    logger(f"Requested URL: {request.data['url']} Shortened URL: {response}")
    return {'url': response}


@action(detail=False, methods=['get'], url_path='redirect')
def redirect(request):
    short_url_id = request.data['id']
    response = get_long_url(short_url_id)
    if response:
        increment_visits(short_url_id)
        return {'url': response}
    logger(f"Short URL: {short_url_id} doesn't exist")
    return Http404("Short URL doesn't exist")

@action(detail=False, methods=['post'], url_path='stats')
def stats(request):
    short_url = request.data['url']
    if not check_if_short_url_exists(short_url):
        logger(f"Stats ::: Short URL: {short_url} doesn't exist")
        return Http404("Short URL doesn't exist")
    response = get_short_url_stats(short_url)
    return {'stats': response}