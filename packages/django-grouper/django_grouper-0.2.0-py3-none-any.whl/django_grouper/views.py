from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import get_object_or_404
from django.views.generic.base import TemplateView
from django.http import HttpResponseRedirect


from .utils import group_queryset


class BaseView(TemplateView):
    def dispatch(self, request, *args, **kwargs):
        app_label, model = request.GET.get("group_content_type", ".").split(".")
        self.django_content_type = get_object_or_404(
            ContentType, app_label=app_label, model=model
        )
        return super().dispatch(request, *args, **kwargs)


class Grouper(BaseView):
    template_name = "django_grouper/grouper.html"

    def get_context_data(self, *args, **kwargs):
        fields = self.request.GET.getlist("group_fields", [])

        ctx = super().get_context_data(*args, **kwargs)
        ctx["content_type"] = self.django_content_type
        ctx["groups"] = group_queryset(self.get_queryset(), fields)
        return ctx

    def get_queryset(self):
        qs = self.django_content_type.model_class().objects.all()
        if hasattr(settings, "GROUP_FILTER"):
            qs = settings.GROUP_FILTER(qs, self.request)
        return qs


class Group(BaseView):
    template_name = "django_grouper/group.html"

    def get_context_data(self, *args, **kwargs):
        ids = self.request.GET.getlist("ids", [])

        ctx = super().get_context_data(*args, **kwargs)
        ctx["content_type"] = self.django_content_type
        ctx["title"] = self.request.GET.get("group_title")
        ctx["object_list"] = self.django_content_type.model_class().objects.filter(
            pk__in=ids
        )
        return ctx

    def post(self, request, *args, **kwargs):
        ctx = self.get_context_data()
        ctx["merged_ids"] = []
        primary = request.POST.get("primary")
        primaryobj = self.django_content_type.model_class().objects.get(pk=primary)
        for merge_id in request.POST.getlist("to_merge"):
            mergeobject = get_object_or_404(
                self.django_content_type.model_class(), pk=merge_id
            )
            mergeobject.grouped_into = primaryobj
            mergeobject.save()
            ctx["merged_ids"].append(merge_id)
        return HttpResponseRedirect(primaryobj.get_absolute_url())
