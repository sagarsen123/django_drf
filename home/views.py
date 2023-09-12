from rest_framework.decorators import api_view
from rest_framework.response import Response
from home.models import *
from home.serializer import PeopleSerializer


@api_view(['GET', 'POST'])
def index(request):
    if request.method == "GET":
        json_response = {
            'name' : 'scalar',
            'courses' : ['C++', 'Python'],
            'method' : 'GET'
        }
    else:
        data = request.data
        print(data)
        json_response = {
            'name' : 'Scalar',
            'courses' : ['C++', 'Python'],
            'method' : 'POST'
        }
    
    return Response(json_response)


@api_view(['GET', 'POST', 'PUT', 'PATCH', 'DELETE'])
def people(request):
    if request.method == 'GET':
        # show only those entries having color entry
        # objs = Person.objects.filter(color__isnull = False)
        objs = Person.objects.all()
        seralizer = PeopleSerializer(objs, many = True)
        print('in')
        return Response(seralizer.data)
    elif request.method == 'POST':
        data = request.data 
        seralizer = PeopleSerializer(data = data)
        print('out')
        # checks if the data send is correct or not
        # if the received data is correct the object is creaed
        if seralizer.is_valid():
            seralizer.save()
            return Response(seralizer.data)
        # else the serializer error is returned
        return Response(seralizer.errors)
    elif request.method == 'PUT':
        # suppoprts only full update
        data = request.data
        obj = Person.objects.get(id = data['id'])
        seralizer = PeopleSerializer(obj, data = data)
        if seralizer.is_valid():
            seralizer.save()
            return Response(seralizer.data)
        return Response(seralizer.errors)
    elif request.method == 'PATCH':
        #also supports partial update
        data = request.data
        obj = Person.objects.get(id = data['id'])
        seralizer = PeopleSerializer(obj, data = data, partial = True)
        if seralizer.is_valid():
            seralizer.save()
            return Response(seralizer.data)
        return Response(seralizer.errors)
    elif request.method == 'DELETE':
        data = request.data
        obj = Person.objects.get(id = data['id'])
        obj.delete()
        return Response({'message' : 'Person Deleted'})







































# @api_view(['GET', 'POST', 'PUT'])
# def index(request):
#     if request.method == 'GET':
#         print(request.GET.get('search'))
#         courses = {
#             'course_name' : 'Python',
#             'learn' : ['flask', 'Django', 'Tornado', 'FastApi'],
#             'course_provider' : 'Scaler',
#         }
#         return Response(courses)
#     elif request.method == 'POST':
#         data = request.data
#         print(data['name'])
#         print('Post Method')
#         return Response('You hitted a POST Method')
#     elif request.method == 'PUT':
#         print('Put MEthod')
#         return Response('You just hitted the Put Method')