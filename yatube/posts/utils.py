from django.core.paginator import Paginator


POSTS_FOR_TEST = 15
POSTS_PER_PAGE = 10


def post_paginator(queryset, request):
    paginator = Paginator(queryset, POSTS_PER_PAGE)
    page_number = request.GET.get('page')
    return paginator.get_page(page_number)
