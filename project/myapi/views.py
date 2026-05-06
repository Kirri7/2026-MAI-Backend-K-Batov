from django.shortcuts import render
from django.http import JsonResponse

def get_profile(request):
    data = {
        "user": "Some Human",
        "email": "some@hum.an",
        "balance": 1500.0
    }
    return JsonResponse(data)

def get_products(request):
    data = {
        "products": [
            {"id": 1, "name": "sticker", "price": 10},
            {"id": 2, "name": "pencil", "price": 20},
        ]
    }
    return JsonResponse(data)

def get_category(request, category_id):
    data = {
        "category_id": category_id,
        "category_name": "office",
        "items_count": 2
    }
    return JsonResponse(data)