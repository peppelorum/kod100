from django.db import models

from utils import choices

FILTER_ON_CHOICES = choices(
    (1, 'Title'),
    (2, 'Body'),
)

class Filter(models.Model):
    title = models.CharField(max_length=255)
    filter_on = models.IntegerField(choices=FILTER_ON_CHOICES)
    regex = models.CharField(max_length=255)
    ignore_case = models.BooleanField(default=True)

    def __unicode__(self):
        return self.title

    class Meta:
        ordering = ('title',)

class Category(models.Model):
    name = models.CharField(max_length=64)
    slug = models.SlugField(unique=True, max_length=64)

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ('name',)
        verbose_name_plural = 'categories'

class FeedManager(models.Manager):
    def unread(self):
        return self.get_query_set().filter(posts__read=False).distinct()

class Feed(models.Model):
    title = models.CharField(max_length=256)
    category = models.ForeignKey(Category, default=1)
    dt_checked = models.DateTimeField()
    dt_updated = models.DateTimeField()
    url = models.URLField()
    feed_url = models.URLField()
    error = models.IntegerField(blank=True, null=True)
    filters = models.ManyToManyField(Filter, blank=True, null=True)

    objects = FeedManager()

    def __unicode__(self):
        return self.title

    def unread_posts(self):
        return self.posts.filter(read=False)

    def count_unread(self):
        return self.unread_posts().count()

    def count_total(self):

        return self.posts.count()
    class Meta:
        ordering = ('category', 'title',)

class Post(models.Model):
    guid = models.CharField(max_length=255, unique=True)
    feed = models.ForeignKey(Feed, related_name='posts')
    dt_published = models.DateTimeField()
    dt_cached = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=256)
    author = models.CharField(max_length=256)
    content = models.TextField()
    link = models.URLField(max_length=512)
    read = models.BooleanField(default=False)
    saved = models.BooleanField(default=False)
    current = models.BooleanField(default=True)

    def __unicode__(self):
        return self.title

    class Meta:
        ordering = ('-dt_published', '-dt_cached')

