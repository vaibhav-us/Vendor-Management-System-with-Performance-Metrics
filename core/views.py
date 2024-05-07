from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework import status
from .models import Vendor,PO,Performance
from .serializers import POSerializer,VendorSerializer,PerformanceSerializer
from django.utils import timezone
from datetime import timedelta
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate


#function for updating reponse time
#Average response is set to hours
def update_response_time(vendor):
    response_time =timedelta()
    total_po =0
    po_list = PO.objects.filter(vendor=vendor, acknowledgement_date__isnull = False)
    for po in po_list:
        response_time += (po.acknowledgement_date - po.issue_date)
        total_po += 1
    avg_response_time = (response_time.total_seconds()/3600)/total_po
    
    performance,_ = Performance.objects.get_or_create(vendor=vendor)
    performance.avg_response_time = avg_response_time
    performance.save()

    vendor.avg_response_time = avg_response_time
    vendor.save()
    
    print("response time upadated")
    print(avg_response_time)

#function for updating average quality rating
def update_avg_quality_rating(vendor):
    quality_rate = 0.0

    toatal_po = 0
    po_list = PO.objects.filter(vendor=vendor, quality_rating__isnull = False)
    for po in po_list:
        quality_rate += po.quality_rating
        toatal_po += 1
    avg_quality_rating = (quality_rate/toatal_po)
    performance = Performance.objects.get(vendor=vendor)
    performance.quality_rating_avg = avg_quality_rating
    performance.save()

    vendor.quality_rating_avg = avg_quality_rating
    vendor.save()

#function for updating fulfillment rate
def update_fulfillment_rate(vendor):
    
    fulfilled_orders = PO.objects.filter(vendor=vendor,status="completed").count()
    issued_orders = PO.objects.filter(vendor=vendor).count()

    fulfillment_rate = (fulfilled_orders/issued_orders)*100
    
    performance,_ = Performance.objects.get_or_create(vendor=vendor)
    performance.fulfillment_rate = fulfillment_rate 
    performance.save()

    vendor.fulfillment_rate = fulfillment_rate
    vendor.save()
 

#function for updating on time delivery date
def update_on_time_delivery_rate(vendor):

    completed_orders = PO.objects.filter(vendor=vendor,status="completed")
    total_completed_orders = completed_orders.count()

    total_on_time_delivery = completed_orders.filter(in_time_delivery = True).count()
    
    on_time_delivery_rate = (total_on_time_delivery/total_completed_orders)*100 if total_completed_orders != 0 else 0.0
    
    performance,_ = Performance.objects.get_or_create(vendor=vendor)
    performance.on_time_delivery_rate = on_time_delivery_rate
    performance.save()

    vendor.on_time_delivery_rate = on_time_delivery_rate
    vendor.save()


#Api endpoint for creating and listing vendors
@api_view(['POST','GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def vendors_create_list(request):
    if request.method == 'GET':
        vendors = Vendor.objects.all()
        serializer = VendorSerializer(vendors, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = VendorSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

#Api endpoint for  retreiving, updating and deleting vendors 
@api_view(['GET', 'PUT', 'DELETE'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def vendors_retrieve_update_destroy(request,id):
    try:
        vendor = Vendor.objects.get(id = id)
    except Vendor.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = VendorSerializer(vendor)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = VendorSerializer(vendor, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        vendor.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


#Api endpoint for creating and listing purchase orders
@api_view(['POST','GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def po_create_list(request):
    if request.method == 'GET':
        purchase_orders = PO.objects.all()
        serializer = POSerializer(purchase_orders, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = POSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)





#Api endpoint for retreiving, updating and deleting purchase orders
@api_view(['GET','PUT','DELETE'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def po_retreive_update_delete(request,id):
    try:
        purchase_order = PO.objects.get(id=id)
    except PO.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        serializer = POSerializer(purchase_order)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = POSerializer(purchase_order,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        purchase_order.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


#Api endpoint for getting vendor performance
@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def vendor_performance(request,id):
    try:
        vendor  = Vendor.objects.get(id=id)
        vendor_pfm = Performance.objects.get(vendor=vendor)
        serializer = PerformanceSerializer(vendor_pfm)
    except Vendor.DoesNotExist or Performance.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    return Response(serializer.data)



#Api endpoint for acknowledging purchase orders
#Delivery date is automatically set to one day after acknowledge date
@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def acknowledge_orders(request,id):
    post_order = PO.objects.get(id=id)
    post_order.acknowledgement_date = timezone.now()
    post_order.delivery_date = timezone.now() + timedelta(days=1)
    post_order.save()
    serializer = POSerializer(post_order)
    return Response(serializer.data)



#Api endpoint for login and to generate token
@api_view(['POST'])
def login(request):
    username = request.data.get('username')
    password = request.data.get('password')
    user = 'hi'
    user = authenticate(username=username, password=password)
    if user:
        # User authenticated, generate or retrieve token
        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key})
    else:
        # Authentication failed
        return Response({'error': 'Invalid credentials'}, status=400)
    

#Api endpoint for log out and to delete token 
@api_view(['POST'])
def logout(request):
    
    token = request.data.get('token')

    if token:
        try:
            token = Token.objects.get(key=token)
        except Token.DoesNotExist:
            return Response({'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)

        # Delete token
        token.delete()
        return Response({'message': 'Logout successful'})
    else:
        return Response({'error': 'Token required'}, status=status.HTTP_400_BAD_REQUEST)