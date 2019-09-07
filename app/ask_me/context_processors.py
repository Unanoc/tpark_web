from ask_me.models import User, Tag
from django.core.cache import cache


def add_tags_users_to_context(request):
  if cache.get('top_users') and cache.get('top_tags'):
    print('Data is from cache')
    return cache.get_many(['top_users', 'top_tags'])
  else:
    print('Data is not from cache')
    top_users = User.objects.by_rating()[:5]
    top_tags = Tag.objects.hottest()[:9]
    return {'top_users': top_users, 'top_tags': top_tags}