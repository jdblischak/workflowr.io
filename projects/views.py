from django.http import Http404
from django.shortcuts import render
from django.views import generic

from .models import Author, Platform, Project, Publication, Tag


def index(request):
    return render(request, 'index.html')


class AuthorList(generic.ListView):
    model = Author


class AuthorDetail(generic.DetailView):
    model = Author

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['project_list_for_author'] = Project.objects.filter(
            author=context['author'])
        return context

    def get_object(self, queryset=None):
        if queryset is None:
            queryset = self.get_queryset()

        platform_slug = self.kwargs.get('platform_slug', None)
        author_slug = self.kwargs.get('author_slug', None)
        try:
            obj = queryset.get(
                name=author_slug, project__platform__name=platform_slug)
        except queryset.model.DoesNotExist:
            raise Http404("No Author found matching the query")
        return obj


class ProjectList(generic.ListView):
    model = Project


class ProjectDetail(generic.DetailView):
    model = Project

    def get_object(self, queryset=None):
        if queryset is None:
            queryset = self.get_queryset()

        platform_slug = self.kwargs.get('platform_slug', None)
        author_slug = self.kwargs.get('author_slug', None)
        project_slug = self.kwargs.get('project_slug', None)
        try:
            obj = queryset.get(
                name=project_slug, author__name=author_slug,
                platform__name=platform_slug)
        except queryset.model.DoesNotExist:
            raise Http404("No Author found matching the query")
        return obj


class TagList(generic.ListView):
    model = Tag


class TagDetail(generic.DetailView):
    model = Tag
    slug_field = 'name'
    slug_url_kwarg = 'name'


class PublicationList(generic.ListView):
    model = Publication


class PlatformDetail(generic.DetailView):
    model = Platform

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['project_list_for_platform'] = Project.objects.filter(
            platform=context['platform'])
        return context

    def get_object(self, queryset=None):
        if queryset is None:
            queryset = self.get_queryset()

        platform_slug = self.kwargs.get('platform_slug', None)
        try:
            obj = queryset.get(name=platform_slug)
        except queryset.model.DoesNotExist:
            raise Http404("No Platform found matching the query")
        return obj
