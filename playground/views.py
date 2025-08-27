from django.shortcuts import render
from django.core.cache import cache
import requests


def say_hello(request):
    key = 'httpbin_result'

    if cache.get(key) is None:
        response = requests.get('https://httpbin.org/delay/2')
        data = response.json()
        cache.set(key, data)
    return render(request, "hello.html", {"name": cache.get(key)})