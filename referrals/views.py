from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .serializers import ReferralPostSerializer
from rest_framework.generics import ListAPIView
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from .models import Application, ReferralPost
from django.contrib import messages

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
        job_id = request.POST.get("job_id")
        description = request.POST.get("description")
        slots = request.POST.get("available_slots")

        ReferralPost.objects.create(
            referrer=request.user,
            company=profile.company,
            job_id=job_id,
            job_title=job_title,
            description=description,
            available_slots=slots
        )

        return redirect("/api/referrals/posts-page/")

    return render(request, "create_post.html", {
        "company": profile.company
    })



@login_required
def apply_referral(request, referral_id):
    referral = get_object_or_404(ReferralPost, id=referral_id)
    user = request.user

    # Prevent applying to your own post
    if referral.referrer == user:
        messages.error(request, "You cannot apply to your own referral post.")
        return redirect("posts_page")

    # Prevent duplicate application
    if Application.objects.filter(referral=referral, applicant=user).exists():
        messages.warning(request, "You have already applied for this referral.")
        return redirect("posts_page")

    # Prevent applying if post is closed
    if not referral.is_open:
        messages.error(request, "This referral is closed.")
        return redirect("posts_page")

    if request.method == "POST":
        why_refer = request.POST.get("why_refer")
        why_company = request.POST.get("why_company")

        if not hasattr(user, "profile") or not user.profile.resume:
            messages.error(request, "Please upload your resume in profile before applying.")
            return redirect("profile")

        Application.objects.create(
            referral=referral,
            applicant=user,
            full_name=user.username,
            email=user.email,
            resume=user.profile.resume,
            why_refer=why_refer,
            why_company=why_company
        )

        messages.success(request, "Application submitted successfully.")
        return redirect("posts_page")

    return render(request, "apply_referral.html", {"referral": referral})


@login_required
def my_applications_dashboard(request):
    applications = Application.objects.filter(
        applicant=request.user
    ).select_related("referral")

    return render(request, "my_applications.html", {
        "applications": applications
    })

@login_required
def my_posts_dashboard(request):
    posts = ReferralPost.objects.filter(referrer=request.user)

    return render(request, "my_posts.html", {
        "posts": posts
    })


@login_required
def post_applicants(request, post_id):
    post = get_object_or_404(
        ReferralPost,
        id=post_id,
        referrer=request.user
    )

    applications = Application.objects.filter(
        referral=post
    ).select_related("applicant")

    return render(request, "post_applicants.html", {
        "post": post,
        "applications": applications
    })

@login_required
def update_application_status(request, app_id, action):
    application = get_object_or_404(
        Application,
        id=app_id,
        referral__referrer=request.user
    )

    referral = application.referral

    if application.status != "PENDING":
        return redirect("post_applicants", post_id=referral.id)

    if action == "accept":
        if referral.available_slots > 0:
            application.status = "APPROVED"
            referral.available_slots -= 1
            referral.save()
            application.save()

            # 🔥 AUTO REJECT IF NO SLOTS LEFT
            if referral.available_slots == 0:
                Application.objects.filter(
                    referral=referral,
                    status="PENDING"
                ).update(status="REJECTED")

    elif action == "reject":
        application.status = "REJECTED"
        application.save()

    return redirect("post_applicants", post_id=referral.id)

@login_required
def profile_detail(request, user_id):
    user_obj = get_object_or_404(settings.AUTH_USER_MODEL, id=user_id)
    return render(request, "profile_detail.html", {"profile_user": user_obj})

@login_required
def candidate_detail(request, app_id):
    application = get_object_or_404(
        Application,
        id=app_id,
        referral__referrer=request.user
    )

    return render(request, "candidate_detail.html", {
        "application": application
    })