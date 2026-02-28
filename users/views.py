from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import RegisterSerializer

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import Profile

class RegisterView(APIView):

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "User registered successfully"},
                status=status.HTTP_201_CREATED
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
from rest_framework.permissions import IsAuthenticated

class ProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({
            "username": request.user.username,
            "role": request.user.role,
            "company": request.user.company
        })


@login_required
def profile_view(request):
    profile = request.user.profile

    if request.method == "POST":
        profile.phone_number = request.POST.get("phone_number")
        profile.current_location = request.POST.get("current_location")
        profile.role = request.POST.get("role")
        profile.company = request.POST.get("company")
        profile.designation = request.POST.get("designation")
        profile.github = request.POST.get("github")
        profile.linkedin = request.POST.get("linkedin")
        profile.portfolio = request.POST.get("portfolio")

        if request.FILES.get("resume"):
            profile.resume = request.FILES.get("resume")

        profile.save()
        return redirect("/")

    return render(request, "profile.html", {"profile": profile})