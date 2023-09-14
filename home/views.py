from rest_framework.decorators import api_view
from rest_framework.response import Response
from home.models import *
from home.serializer import *
from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication

from django.contrib.auth import authenticate

# for pagination 
from django.core.paginator import Paginator



# actions enclose the things related to a specified view (apis in one class)
# it is a decorator
from rest_framework.decorators import action

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


@api_view(['POST'])
def login(request):
    data = request.data
    serializer = LoginSerializer(data = data)

    if serializer.is_valid():
        data = serializer.data
        print(data)
        return Response({'message':'Login Successful'})
    return Response(serializer.errors)


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



class PersonApi(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    def get(self, request):
        objs = Person.objects.all()

        try:
            # making pagination
            page = request.GET.get('page', 1)
            pagesize = 3
            paginator = Paginator(objs, pagesize)
            seralizer = PeopleSerializer(paginator.page(page), many = True)
            # seralizer = PeopleSerializer(objs, many = True)
            print('in')
            return Response(seralizer.data)
        except Exception as e:
            return Response({'status': False, 'message': 'Invalid Page'})


    def post(self, request):
        data = request.data 
        seralizer = PeopleSerializer(data = data)
        print('out')
        if seralizer.is_valid():
            seralizer.save()
            return Response(seralizer.data)
        return Response(seralizer.errors)
    
    def put(self, request):
        data = request.data
        obj = Person.objects.get(id = data['id'])
        seralizer = PeopleSerializer(obj, data = data)
        if seralizer.is_valid():
            seralizer.save()
            return Response(seralizer.data)
        return Response(seralizer.errors)

    def patch(self, request):
        data = request.data
        obj = Person.objects.get(id = data['id'])
        seralizer = PeopleSerializer(obj, data = data, partial = True)
        if seralizer.is_valid():
            seralizer.save()
            return Response(seralizer.data)
        return Response(seralizer.errors)

    def delete(self, request):
        data = request.data
        obj = Person.objects.get(id = data['id'])
        obj.delete()
        return Response({'message' : 'Person Deleted'})


class PeopleViewSet(viewsets.ModelViewSet):
    serializer_class = PeopleSerializer
    queryset = Person.objects.all()
    http_method_names = ['get', 'post']

    def list(self, request):
        search = request.GET.get('search')
        queryset = self.queryset
        if search:
            queryset = queryset.filter(name__startswith = search)
        serializer = PeopleSerializer(queryset, many = True)
        return Response({'status': 200, 'data': serializer.data}, status=status.HTTP_204_NO_CONTENT)
    
    # this to use the action decorator
    @action(detail=True, methods=['post'])
    def send_mail_to_person(self, request, pk):
        obj = Person.objects.get(pk = pk)
        serializer = PeopleSerializer(obj)
        print(pk)
        return Response({'status': True, 'message': "Mail sent successfully", 'data' : serializer.data}, status=status.HTTP_200_OK)
    


# token authentication part
class RegisterAPI(APIView):
    def post(self, request):
        data = request.data
        serializer = RegisterSerializer(data = data)

        if not serializer.is_valid():
            return Response({'status':False, 'message': serializer.errors}, status.HTTP_400_BAD_REQUEST)
        
        serializer.save()

        return Response({'status': 200, 'message' : 'user created successfully'}, status.HTTP_201_CREATED)


class LoginAPI(APIView):
    def post(self, request):
        data = request.data
        serializer = LoginSerializer(data = data)

        if not serializer.is_valid():
            return Response({'status':False, "message": serializer.errors}, status.HTTP_400_BAD_REQUEST)
        

        user = authenticate(username = serializer.data["username"] , password = serializer.data["password"])

        if not user:
            Response({'status':False, "message": "Invalid Credentials"}, status.HTTP_404_NOT_FOUND)

        token, _ = Token.objects.get_or_create(user=user)

        return Response({'status':200, 'message': 'logged in sucessfully', 'token' : str(token)}, status.HTTP_200_OK)



























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