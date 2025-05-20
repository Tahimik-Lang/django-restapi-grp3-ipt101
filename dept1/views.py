from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import ChartData
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import json

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

def chart_data(request):
    data = list(ChartData.objects.values())
    return JsonResponse(data, safe=False)


from django.shortcuts import render
from django.db.models import Count
from .models import ChartData

@api_view(['GET'])
def analytics_dashboard(request):
    # Get counts for each preferred category
    category_counts = (ChartData.objects
                       .values('preferred_category')
                       .annotate(count=Count('id'))
                       .exclude(preferred_category__isnull=True)
                       .exclude(preferred_category='')
                       .order_by('-count'))

    # Calculate total votes
    total_votes = sum(item['count'] for item in category_counts)

    # Calculate percentages
    for item in category_counts:
        item['percentage'] = round((item['count'] / total_votes * 100), 1) if total_votes > 0 else 0

    context = {
        'category_counts': category_counts,
        'total_votes': total_votes,
    }
    return render(request, 'home.html', context)

# API Endpoint - Fetch All Data
@api_view(['GET'])
def chart_data(request):
    data = ChartData.objects.all().values('id', 'category', 'value', 'chart_type', 'username', 'preferred_category')
    return Response(list(data))

# API Endpoint - Add New Data
@api_view(['POST'])
def add_chart_data(request):
    category = request.data.get('category')
    value = request.data.get('value')
    chart_type = request.data.get('chart_type')
    username=request.data.get('username', 'anonymous'), # Default to "anonymous" if no username
    preferred_category = request.data.get('preferred_category')
    if category and value and chart_type and username and preferred_category:
        ChartData.objects.create(category=category, value=value, chart_type=chart_type, username=username, preferred_category=preferred_category)
        return Response({"message": "Chart data added successfully!"}, status=201)

    return Response({"error": "Invalid data"}, status=400)

@require_http_methods(["POST"])
def add_chart_data(request):
    data = json.loads(request.body)
    chart_data = ChartData.objects.create(
        category=data['category'],
        value=data['value'],
        chart_type=data['chart_type'],
        username=["username", "anonymous"],  # Default to "anonymous" if no username
        preferred_category=data['category']  # Use the category as preferred_category
    )
    return JsonResponse({'id': chart_data.id})


# API Endpoint - Update Existing Data
@api_view(['PUT'])
def update_chart_data(request, id):
    try:
        chart_entry = ChartData.objects.get(id=id)
        chart_entry.category = request.data.get('category', chart_entry.category)
        chart_entry.value = request.data.get('value', chart_entry.value)
        chart_entry.chart_type = request.data.get('chart_type', chart_entry.chart_type)
        chart_entry.username = request.data.get('username', chart_entry.username)
        chart_entry.preferred_category = request.data.get('preferred_category', chart_entry.preferred_category)

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






@csrf_exempt
@require_http_methods(["POST"])
def add_chart_data(request):
    body = json.loads(request.body)
    obj = ChartData.objects.create(
        category=body.get("category"),
        value=body.get("value"),
        chart_type=body.get("chart_type"),
        username=body.get("username", "anonymous"),  # Default to "anonymous" if no username
        preferred_category=body.get('preferred_category')
    )
    return JsonResponse({"id": obj.id, "status": "added"})

@csrf_exempt
@require_http_methods(["PUT"])
def update_chart_data(request, id):
    body = json.loads(request.body)
    ChartData.objects.filter(id=id).update(
        category=body.get("category"),
        value=body.get("value"),
        username=body.get("username", "anonymous"),  # Default to "anonymous" if no username
        preferred_category=body.get("preferred_category")
    )
    return JsonResponse({"id": id, "status": "updated"})

@csrf_exempt
@require_http_methods(["DELETE"])
def delete_chart_data(request, id):
    ChartData.objects.filter(id=id).delete()
    return JsonResponse({"id": id, "status": "deleted"})