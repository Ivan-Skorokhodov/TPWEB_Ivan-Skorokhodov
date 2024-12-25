from django.conf import settings
from django.utils.timezone import now
from datetime import timedelta
from app import models
import jwt
import time
from django.core.cache import cache
from django.db.models import Count, Q


def get_centrifugo_token(user_id):
    claims = {"sub": str(user_id), "exp": int(time.time()) + 5*60}
    token = jwt.encode(
        claims, settings.CENTRIFUGO_SECRET_KEY, algorithm="HS256")
    return {"token": token, "ws_url": settings.CENTRIFUGO_WS_URL}


def cache_popular_tags():
    three_months_ago = now() - timedelta(days=90)

    cache_key = "popular_tags"
    cached_popular_tags = models.Tag.objects.annotate(
        num_questions=Count(
            'question',
            filter=Q(question__created_at__gte=three_months_ago)
        )
    ).order_by('-num_questions')[:10]

    cache_duration = 90 * 24 * 60 * 60  # 90 дней
    cache.set(cache_key, cached_popular_tags, cache_duration)


def get_popular_tags():
    cache_key = "popular_tags"
    cached_popular_tags = cache.get(cache_key)
    return {"popular_tags": cached_popular_tags}


def cache_best_members():
    one_week_ago = now() - timedelta(days=7)

    cache_key = "best_members"
    cached_best_members = models.Profile.objects.annotate(
        num_popular_questions=Count(
            'question',
            filter=Q(
                question__created_at__gte=one_week_ago
            ) & Q(
                question__answer__isnull=False
            )
        )
    ).order_by('-num_popular_questions')[:10]

    cache_duration = 7 * 24 * 60 * 60  # 7 дней
    cache.set(cache_key, cached_best_members, cache_duration)


def get_best_members():
    cache_key = "best_members"
    cached_best_members = cache.get(cache_key)
    return {"best_members": cached_best_members}


def global_settings(request):
    return {**get_centrifugo_token(request.user.id), **get_popular_tags(), **get_best_members()}
