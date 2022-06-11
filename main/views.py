from django.shortcuts import render
from django.http import HttpResponse
import json

def index(request):
    # print(str(request.__dict__))
    # my_json=json.loads(request.__dict__)
    # my_json=json.dumps(request.__dict__)
    my_req=request.body
    # print(type(my_req))
    # print((my_req))
    print(request.COOKIES)
    
    return HttpResponse(str("hello"))