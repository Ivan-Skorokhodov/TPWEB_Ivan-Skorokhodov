from django.conf import settings
import requests
from app import models
import jwt
import time
from django.core.cache import cache
from django.db.models import Count


def get_centrifugo_token(user_id):
    claims = {"sub": str(user_id), "exp": int(time.time()) + 5*60}
    token = jwt.encode(
        claims, settings.CENTRIFUGO_SECRET_KEY, algorithm="HS256")
    return {"token": token, "ws_url": settings.CENTRIFUGO_WS_URL}


def cache_popular_tags():
    cache_key = "popular_tags"
    cached_popular_tags = models.Tag.objects.annotate(
        num_questions=Count('question')).order_by('-num_questions')[:10]
    cache.set(cache_key, cached_popular_tags, 60)


def get_popular_tags():
    cache_key = "popular_tags"
    cached_popular_tags = cache.get(cache_key)
    return {"popular_tags": cached_popular_tags}


def cache_best_members():
    cache_key = "best_members"
    cached_best_members = models.Profile.objects.annotate(
        num_answers=Count('answer')).order_by('-num_answers')[:10]
    cache.set(cache_key, cached_best_members, 60)


def get_best_members():
    cache_key = "best_members"
    cached_best_members = cache.get(cache_key)
    return {"best_members": cached_best_members}


def global_settings(request):
    return {**get_centrifugo_token(request.user.id), **get_popular_tags(), **get_best_members()}
