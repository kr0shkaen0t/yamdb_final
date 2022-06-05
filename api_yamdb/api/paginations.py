from rest_framework.pagination import PageNumberPagination


class ReviewsSetPagination(PageNumberPagination):
    page_size = 5


class CommentSetPagination(PageNumberPagination):
    page_size = 5
