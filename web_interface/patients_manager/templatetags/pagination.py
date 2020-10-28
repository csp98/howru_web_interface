from django import template

from web_interface.core import settings

register = template.Library()


@register.filter
def paginate(paginator, current):
    """
    Construct a proper pagination menu
    https://medium.com/@sumitlni/paginate-properly-please-93e7ca776432
    """
    num_pages = settings.PAGE_SIZE
    if paginator.num_pages > 2 * num_pages:
        start = max(1, current - num_pages)
        end = min(paginator.num_pages, current + num_pages)
        if end < start + 2 * num_pages:
            end = start + 2 * num_pages
        elif start > end - 2 * num_pages:
            start = end - 2 * num_pages
        if start < 1:
            end -= start
            start = 1
        elif end > paginator.num_pages:
            start -= (end - paginator.num_pages)
            end = paginator.num_pages
        pages = [page for page in range(start, end + 1)]
        return pages[:(2 * num_pages + 1)]
    return paginator.page_range
