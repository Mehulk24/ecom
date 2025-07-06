from django.shortcuts import render,redirect
from django.http import HttpResponseNotFound
from django.urls import resolve, Resolver404

class Custom404Middleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        try:
            resolve(request.path_info)
        except Resolver404:
            # Redirect to a custom 404 view at /404/
            return redirect('/404/')

        response = self.get_response(request)
        return response