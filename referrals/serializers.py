from rest_framework import serializers
from .models import ReferralPost


class ReferralPostSerializer(serializers.ModelSerializer):

    class Meta:
        model = ReferralPost
        fields = '__all__'
        read_only_fields = ['referrer']

    def create(self, validated_data):
        validated_data['referrer'] = self.context['request'].user
        return super().create(validated_data)

from .models import ReferralApplication


class ReferralApplicationSerializer(serializers.ModelSerializer):

    class Meta:
        model = ReferralApplication
        fields = ['id', 'referral_post', 'message']
        read_only_fields = ['candidate']

    def validate(self, data):
        user = self.context['request'].user
        referral_post = data['referral_post']

        # ❌ prevent self-apply
        if referral_post.referrer == user:
            raise serializers.ValidationError(
                "You cannot apply to your own referral post."
            )

        # ❌ prevent duplicate apply
        if ReferralApplication.objects.filter(
                referral_post=referral_post,
                candidate=user
        ).exists():
            raise serializers.ValidationError(
                "You have already applied to this referral post."
            )

        return data

    def create(self, validated_data):
        validated_data['candidate'] = self.context['request'].user
        return super().create(validated_data)