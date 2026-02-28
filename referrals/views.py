from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from .models import ReferralPost
from .serializers import ReferralPostSerializer

from rest_framework.generics import ListAPIView

from django.shortcuts import render
from .models import ReferralPost

from django.shortcuts import render, redirect
from .models import ReferralPost
from django.contrib.auth.decorators import login_required

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import ReferralPost


class CreateReferralPostView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = ReferralPostSerializer(
            data=request.data,
            context={'request': request}
        )

        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "Referral post created"},
                status=status.HTTP_201_CREATED
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


class ReferralPostListView(ListAPIView):
    queryset = ReferralPost.objects.all()
    serializer_class = ReferralPostSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        company = self.request.query_params.get('company')

        if company:
            queryset = queryset.filter(company__icontains=company)

        return queryset
    
@login_required
def post_list_page(request):
    posts = ReferralPost.objects.all()
    return render(request, "posts.html", {"posts": posts})



@login_required
def create_post_page(request):

    profile = request.user.profile

    # Prevent posting if company not filled
    if not profile.company:
        return render(request, "create_post.html", {
            "error": "Please update your profile with company information first."
        })

    if request.method == "POST":
        job_title = request.POST.get("job_title")
        description = request.POST.get("description")
        slots = request.POST.get("available_slots")

        ReferralPost.objects.create(
            referrer=request.user,
            company=profile.company,   # 🔒 locked
            job_title=job_title,
            description=description,
            available_slots=slots
        )

        return redirect("/api/referrals/posts-page/")

    return render(request, "create_post.html", {
        "company": profile.company
    })