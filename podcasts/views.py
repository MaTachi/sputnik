from django.shortcuts import get_object_or_404
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from podcasts import models


class Podcasts(ListView):
    model = models.Podcast
    template_name = 'podcasts/podcasts.html'


class Podcast(ListView):
    template_name = 'podcasts/podcast.html'

    def get_queryset(self):
        self.podcast = get_object_or_404(models.Podcast,
                                         pk=self.kwargs['podcast'])
        return models.Episode.objects.filter(podcast=self.podcast)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['podcast'] = self.podcast
        return context


class Episode(DetailView):
    template_name = 'podcasts/episode.html'

    def get_object(self):
        podcast = get_object_or_404(models.Podcast, pk=self.kwargs['podcast'])
        episode = int(self.kwargs['episode']) - 1
        return models.Episode.objects.filter(podcast=podcast)[episode]
