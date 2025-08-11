from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializer import ProductSerializer, CollectionSerializer
from rest_framework import status
from rest_framework.views import APIView
from .models import Product, Collection
from django.db.models import Count


class ProductList(APIView):
    def get(self, request):
        queryset = Product.objects.select_related('collection').all()
        serializer = ProductSerializer(queryset, many=True, context={'request': request})
        return Response(serializer.data)
    
    def post(self, request):
        serializer = ProductSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

        
class ProductDetail(APIView):
    def get(self, request, id):
        product = get_object_or_404(Product, pk=id)
        serializer = ProductSerializer(product)
        return Response(serializer.data)
    
    def put(self, request, id):
        product = get_object_or_404(Product, pk=id)
        serializer = ProductSerializer(product, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    
    def delete(self, request, id):
        product = get_object_or_404(Product, pk=id)
        if product.orderitems.count() > 0: # type: ignore
            return Response({'error': 'Cannot delete product with associated order items.'}, status=status.HTTP_400_BAD_REQUEST)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CollectionList(APIView):
    def get(self, request):
        queryset = Collection.objects.annotate(product_count=Count('products')).all()
        serializer = CollectionSerializer(queryset, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = CollectionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
        

class CollectionDetail(APIView):
    def get(self, request, pk):
        collection = get_object_or_404(Collection.objects.annotate(product_count=Count('products')), pk=pk)
        serializer = CollectionSerializer(collection)
        return Response(serializer.data)
    
    def put(self, request,pk):
        collection = get_object_or_404(Collection.objects.annotate(product_count=Count('products')), pk=pk)
        serializer = CollectionSerializer(collection, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def delete(self, request, pk):
        collection = get_object_or_404(Collection.objects.annotate(product_count=Count('products')), pk=pk)
        if collection.product_count > 0: # type: ignore
            return Response({'error': 'Cannot delete a collection that contains products.'}, status=status.HTTP_400_BAD_REQUEST)
        collection.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
  
        