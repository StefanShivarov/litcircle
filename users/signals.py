from allauth.socialaccount.signals import social_account_added, social_account_updated
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Profile


@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    elif hasattr(instance, 'profile'):
        instance.profile.save()


@receiver([social_account_added, social_account_updated])
def populate_social_profile_data(sender, request, sociallogin, **kwargs):
    user = sociallogin.user
    if sociallogin.account.provider != 'google':
        return
    
    picture_url = sociallogin.account.extra_data.get('picture')
    if not picture_url:
        return
    
    profile = getattr(sociallogin.user, 'profile', None)
    if profile and not profile.image:
        profile.social_image_url = picture_url
        profile.save()
