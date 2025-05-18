from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import ChartData

# Page Views
def home(request):
    return render(request, 'home.html')

def pie_chart(request):
    return render(request, 'pie.html')

def bar_chart(request):
    return render(request, 'bar.html')

def doughnut_chart(request):
    return render(request, 'doughnut.html')

def line_chart(request):
    return render(request, 'line.html')

# API Endpoint - Fetch All Data
@api_view(['GET'])
def chart_data(request):
    data = ChartData.objects.all().values('id', 'category', 'value', 'chart_type')
    return Response(list(data))

# API Endpoint - Add New Data
@api_view(['POST'])
def add_chart_data(request):
    category = request.data.get('category')
    value = request.data.get('value')
    chart_type = request.data.get('chart_type')

    if category and value and chart_type:
        ChartData.objects.create(category=category, value=value, chart_type=chart_type)
        return Response({"message": "Chart data added successfully!"}, status=201)

    return Response({"error": "Invalid data"}, status=400)

# API Endpoint - Update Existing Data
@api_view(['PUT'])
def update_chart_data(request, id):
    try:
        chart_entry = ChartData.objects.get(id=id)
        chart_entry.category = request.data.get('category', chart_entry.category)
        chart_entry.value = request.data.get('value', chart_entry.value)
        chart_entry.chart_type = request.data.get('chart_type', chart_entry.chart_type)
        chart_entry.save()
        return Response({"message": "Chart data updated successfully!"})
    except ChartData.DoesNotExist:
        return Response({"error": "Chart data not found"}, status=404)

# API Endpoint - Delete Data
@api_view(['DELETE'])
def delete_chart_data(request, id):
    try:
        chart_entry = ChartData.objects.get(id=id)
        chart_entry.delete()
        return Response({"message": "Chart data deleted successfully!"})
    except ChartData.DoesNotExist:
        return Response({"error": "Chart data not found"}, status=404)


from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
# from .models import ChartData
import json

def chart_data(request):
    data = list(ChartData.objects.values())
    return JsonResponse(data, safe=False)

@csrf_exempt
@require_http_methods(["POST"])
def add_chart_data(request):
    body = json.loads(request.body)
    obj = ChartData.objects.create(
        category=body.get("category"),
        value=body.get("value"),
        chart_type=body.get("chart_type")
    )
    return JsonResponse({"id": obj.id, "status": "added"})

@csrf_exempt
@require_http_methods(["PUT"])
def update_chart_data(request, id):
    body = json.loads(request.body)
    ChartData.objects.filter(id=id).update(
        category=body.get("category"),
        value=body.get("value")
    )
    return JsonResponse({"id": id, "status": "updated"})

@csrf_exempt
@require_http_methods(["DELETE"])
def delete_chart_data(request, id):
    ChartData.objects.filter(id=id).delete()
    return JsonResponse({"id": id, "status": "deleted"})