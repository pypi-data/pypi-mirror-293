Group Django model instances on similar fields

Based on [this tutorial](https://towardsdatascience.com/group-thousands-of-similar-spreadsheet-text-cells-in-seconds-2493b3ce6d8d)

# Installation

1. add `django_grouper` to your `INSTALLED_APPS`
2. add `path("", include("django_grouper.urls"))` to your `urlpatterns`
3. go to `/grouper` and add the param `group_content_type` to specify which ContentType to group and the params `group_fields` to specify which fields to group by

# Configuration

If you define a `GROUP_FILTER` in you settings, the queryset in the `/grouper` view will be passed through this filter. The filter is expected to
be a callable and will receive the queryset and the request as parameters. This means you can pass the queryset together with the request to a
django-filter filter.
