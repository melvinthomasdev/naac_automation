from django.core.exceptions import ObjectDoesNotExist

from rest_framework import status
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView


from .models import User, Document
from .serializers import UserLoginSerializer, UserSerializer, ListDocumentSerializer


@api_view(["POST", ])
@permission_classes([AllowAny, ])
def create_user_view(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        email = serializer.validated_data.get("email")
        password = serializer.validated_data.get("password")
        print(password)
        try:
            user = User.objects.get(email=email)
        except ObjectDoesNotExist:
            user = User.objects.create_user(email=email, password=password)
            # user.set_password(password)
            # user.save()
    else:
        return Response(serializer.errors, status=status.HTTP_409_CONFLICT)
    return Response(
        {
            "message": "Account created",
            "email": user.email,
            "user_id": user.id
        },
        status=status.HTTP_201_CREATED
    )


@api_view(["POST", ])
def login_view(request):
    serializer = UserLoginSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        user.save()

        return Response(
            {
                'user_id': user.pk,
                'email': user.email,
                'token': token.key,
            },
            status=status.HTTP_200_OK
        )
    else:
        try:
            message = serializer.errors['non_field_errors'][0]
        except (IndexError, KeyError) as e:
            message = "Some random message I don't know y"

    return Response({'message': message}, content_type='application/json', status=status.HTTP_400_BAD_REQUEST)


# class ProfileView(APIView):
#
#     permission_classes(IsAuthenticated)
#
#     def post(self, request):
#         print(request.data.dict())
#         try:
#             profile = Profile.objects.get(user=request.user)
#             profile.delete()
#         except ObjectDoesNotExist:
#             pass
#         profile = Profile(user=request.user, **request.data.dict())
#         profile.save()
#         return Response({"message": "Profile Updated"}, status=status.HTTP_200_OK)
#
#     def get(self, request):
#         user = request.user
#         try:
#             profile = Profile.objects.get(user=user)
#         except ObjectDoesNotExist:
#             return Response({"message": "user profile doesn't exist"}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET', ])
@permission_classes([IsAuthenticated, ])
def whoami(request):
    # try:
    #     token = Token.objects.get(key=key)
    #     user = token.user
    # except Token.DoesNotExist:
    #     return Response(
    #         {
    #             "message": "Invalid Token"
    #         },
    #         status=status.HTTP_404_NOT_FOUND
    #     )
    # except User.DoesNotExist:
    #     return Response(
    #         {
    #             "message": "User not found"
    #         },
    #         status=status.HTTP_404_NOT_FOUND
    #     )
    user = request.user

    return Response(
        {
            "id": user.id,
            "username": user.username,
            "email": user.email
        },
        status=status.HTTP_200_OK
    )


@api_view(["GET", ])
@permission_classes([IsAuthenticated, ])
def list_documents_view(request):
    data = []
    user = request.user
    documents = Document.objects.filter(user=user)
    for document in documents:
        data.append({
            "id": document.id,
            "indicator":document.indicator.id,
            "criteria": document.indicator.criterion.id
        })
    return Response(
        {
            "user_id": user.id,
            "documents": data
        },
        status=status.HTTP_200_OK
    )


class DocumentView(APIView):

    permission_classes = [IsAuthenticated]
