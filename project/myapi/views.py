from django.shortcuts import render
from django.http import JsonResponse, HttpResponseNotAllowed

def get_profile(request):
    if request.method == 'POST':
        return JsonResponse({"status": "Profile updated!"})
    elif request.method != 'GET':
        return HttpResponseNotAllowed(['GET', 'POST'])

    data = {
        "user": "Some Human",
        "email": "some@hum.an",
        "balance": 1500.0
    }
    return JsonResponse(data)

def get_products(request):
    if request.method == 'POST':
        return JsonResponse({"status": "Product updated!"})
    elif request.method != 'GET':
        return HttpResponseNotAllowed(['GET', 'POST'])

    data = {
        "products": [
            {"id": 1, "name": "sticker", "price": 10},
            {"id": 2, "name": "pencil", "price": 20},
        ]
    }
    return JsonResponse(data)

def get_category(request, category_id):
    if request.method == 'POST':
        return JsonResponse({"status": "Category updated!"})
    elif request.method != 'GET':
        return HttpResponseNotAllowed(['GET', 'POST'])

    data = {
        "category_id": category_id,
        "category_name": "office",
        "items_count": 2
    }
    return JsonResponse(data)