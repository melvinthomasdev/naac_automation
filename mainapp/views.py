from django.core.exceptions import ObjectDoesNotExist

from rest_framework import status
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView


from .models import User, Criterion,  Indicator, Document
from .serializers import UserLoginSerializer, UserSerializer, DocumentSerializer, CriterionSerializer,\
    IndicatorSerializer, UpdateUserSerializer


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


@api_view(["POST"])
@permission_classes([IsAuthenticated, ])
def complete_profile_view(request):
    data = request.data
    user = request.user
    serializer = UpdateUserSerializer(user, data=data, partial=True)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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
            # "username": user.username,
            "email": user.email,
            "first name": user.first_name,
            "last name": user.last_name,
            "designation": user.designation,
            "department": user.department,
            "college": user.institution
        },
        status=status.HTTP_200_OK
    )


@api_view(["GET", ])
@permission_classes([IsAuthenticated, ])
def list_criteria_view(request):
    criteria = Criterion.objects.all()
    serializer = CriterionSerializer(criteria, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["GET", ])
@permission_classes([IsAuthenticated, ])
def get_criteria_view(request, id):
    try:
        criterion = Criterion.objects.get(id=id)
    except ObjectDoesNotExist:
        return Response(
            {
                "message": "Invalid Criterion ID"
            },
            status=status.HTTP_404_NOT_FOUND
        )
    serializer = CriterionSerializer(criterion)
    return Response(serializer.data, status=status.HTTP_200_OK)
    # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET", ])
@permission_classes([IsAuthenticated, ])
def list_indicator_view(request, criterion_id):
    data = []
    try:
        criterion = Criterion.objects.get(id=criterion_id)
    except ObjectDoesNotExist:
        return Response(
            {
                "message":"Invalid Criterion ID"
            },
            status=status.HTTP_404_NOT_FOUND
        )
    indicators = Indicator.objects.filter(criterion=criterion)
    serializer = IndicatorSerializer(indicators, many=True)
    # for indicator in indicators:
    #     data.append(
    #         {
    #             "criterion_id": indicator.criterion.id,
    #             "indicator_id"
    #         }
    #     )

    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["GET", ])
@permission_classes([IsAuthenticated, ])
def get_indicator_view(request, id):
    try:
        indicator = Indicator.objects.get(id=id)
    except ObjectDoesNotExist:
        return Response(
            {
                "message": "Invalid Indicator ID"
            },
            status=status.HTTP_404_NOT_FOUND
        )
    serializer = IndicatorSerializer(indicator)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["GET", ])
@permission_classes([IsAuthenticated, ])
def list_documents_view(request):
    data = []
    user = request.user
    documents = Document.objects.filter(user=user)
    for document in documents:
        data.append({
            "id": document.id,
            "indicator": document.indicator.id,
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

    def get(self, request, id):
        try:
            document = Document.objects.get(id=id)
        except ObjectDoesNotExist:
            return Response(
                {
                    "message": "Document not found"
                },
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = DocumentSerializer(document)
        return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["POST", ])
@permission_classes([IsAuthenticated, ])
def create_document_view(request):
    content = request.POST.get("content")
    indicator_id = request.POST.get("indicator_id")
    try:
        indicator = Indicator.objects.get(id=indicator_id)
    except ObjectDoesNotExist:
        return Response(
            {
                "message": "Indicator Not Found"
            },
            status=status.HTTP_404_NOT_FOUND
        )
    document, created = Document.objects.get_or_create(user=request.user, indicator=indicator)
    print(created)
    document.content = content
    document.save()
    if created:
        return Response(
            {
                "message": "Document Created",
                "document_id": document.id,
                "indicator_id": document.indicator.id,
            },
            status=status.HTTP_201_CREATED
        )
    return Response(
        {
            "message": "Document Updated",
            "document_id": document.id,
            "indicator_id": document.indicator.id,
        },
        status=status.HTTP_200_OK
    )