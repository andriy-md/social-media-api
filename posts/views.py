from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view(["GET"])
def simple_api_view(request):
    x = 33
    return Response({"number": x})
