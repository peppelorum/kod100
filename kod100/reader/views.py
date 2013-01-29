import urllib2
from urlparse import urljoin
import datetime
import collections

import feedparser
#from BeautifulSoup import BeautifulSoup as BS

from bs4 import BeautifulSoup as BS

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404

from models import Category, Feed, Post
from decorators import view
from feeds import update_feeds
from utils import daterange

ctx = dict

@view(r'^all/$', 'feed_list.html', True)
def all_feeds(request):

    ctx = {
        'category_list': Category.objects.all(),
        'show_all': True
    }

    return ctx

@view(r'^$', 'graph.html', True)
def graph(request):
    start = datetime.date(2013, 1, 27)
    to = datetime.timedelta(days=100)
    end = start + to

    ar = {}

    feeds = Feed.objects.all()

    for feed in feeds:
        user_ar = {}

        r = daterange(start, to=end)
        for a in r:
            count = Post.objects.filter(dt_published__year=a.year, dt_published__month=a.month, dt_published__day=a.day, feed=feed).count()

            if count > 20:
                class_ = '_4'
            elif count > 15 and count <=20:
                class_ = '_3'
            elif count <=15 and count > 10:
                class_ = '_2'
            elif count <= 10 and count > 0:
                class_ = '_1'
            else:
                class_ = '_0'

            user_ar[a] = class_

        od = collections.OrderedDict(sorted(user_ar.items()))
        ar[feed] = od

    ctx = {
        'post_list': Post.objects.all(),
        'table': ar,
        'today': datetime.datetime.today(),
        'show_all': True
    }

    return ctx


@view(r'unread/^$', 'feed_list.html', True)
def unread_feeds(request):
    return ctx(category_list=Category.objects.all())

@view(r'^add/$', True)
def add_feed(request, url=None):
    if url is None:
        url = request.REQUEST['url']
    f = urllib2.urlopen(url)
    soup = BS(f)
    links = [link for link in soup('link', {'rel': 'alternate'})]
    if len(links) > 0:
        feed_url = urljoin(url, links[0]['href'])
        return add_rss(request, feed_url)
    else:
        return add_rss(request, url)

def add_rss(request, url=None):
    if url is None:
        url = request.REQUEST['url']
    d = feedparser.parse(url)
    feed = Feed()
    feed.title = d.feed.get('title', 'Untitled')
    feed.url = d.feed.get('link', url[:url.find('/', 8)])
    feed.feed_url = url
    feed.dt_checked = datetime.datetime(1, 1, 1, 0, 0, 0)
    feed.dt_updated = datetime.datetime(1, 1, 1, 0, 0, 0)
    feed.save()
    update(request, feed.id)
    return HttpResponseRedirect('/admin/reader/feed/%d/' % (feed.id,))


@view(r'^add-github/$', True)
def add_feed_github(request, user=None):
#    if user is None:
#        return 'fail'


    if request.user.is_authenticated():

        user = request.REQUEST['user']
        url = 'https://github.com/%s/' % user
        feed_url = 'https://github.com/%s.atom' % user

    #    feed, create = Feed.objects.get_or_create(title=user)

        category, created = Category.objects.get_or_create(name='github', slug='github')

        feed = Feed()
        feed.title = user
        feed.url = url
        feed.category = category
        feed.feed_url = feed_url
        feed.dt_checked = datetime.datetime(1, 1, 1, 0, 0, 0)
        feed.dt_updated = datetime.datetime(1, 1, 1, 0, 0, 0)
        feed.save()

        return HttpResponse('yay')

#        return HttpResponseRedirect('/admin/reader/feed/%d/' % (feed.id,))
    else:
        return 'h4axx0r..'


@view(r'^(?P<id>\d+)/unread/$', 'post_list.html', True)
def unread(request, id):
    feed = get_object_or_404(Feed, id=id)
    posts = feed.posts.filter(read=False)

    if len(posts) == 0:
        return HttpResponseRedirect('/reader/#f%s' % id)

    return ctx(feed=feed, posts=posts)

@view(r'^post/(?P<id>\d+)/$', 'post.html', True)
def post(request, id):
    post = get_object_or_404(Post, id=id)
    return ctx(post=post)

@view(r'^(?P<id>\d+)/all/$', 'post_list.html', True)
def all(request, id):
    feed = get_object_or_404(Feed, id=id)
    posts = feed.posts.all()

    return ctx(feed=feed, posts=posts)

@view(r'^update/(?P<id>\d+)/$', True)
def update(request, id):
    try:
        feed = Feed.objects.get(id=id)
    except Feed.DoesNotExist:
        return HttpResponseRedirect('/reader/')

    update_feeds(feed)
    return HttpResponseRedirect('/reader/')

@view(r'^update/all/$', True)
def update_all(request):
    for feed in Feed.objects.all():
        update(request, feed.id)
    if request.is_ajax():
        return HttpResponse('Success')
    return HttpResponseRedirect('/reader/')

@view(r'^action/$', True)
def action(request):
    feed = None
    if request.method == 'POST':
        data = request.POST
        post = Post.objects.get(id=data['id'])
        feed = post.feed
        post.read = (data['read'] == '1')
        post.save()
        if data.has_key('ajax'):
            return HttpResponse('Success')
    if not feed or feed.count_unread() == 0:
        return HttpResponseRedirect('/reader/#f%d' % feed.id)
    else:
        return HttpResponseRedirect('/reader/%d/unread/' % feed.id)

@view(r'^action/all/$', True)
def action_all(request):
    feed = None
    if request.method == 'POST':
        data = request.POST
        feed = Feed.objects.get(id=data['id'])
        for post in feed.posts.all():
            post.read = True
            post.save()
        if data.has_key('ajax'):
            return HttpResponse('Success')
    return HttpResponseRedirect('/reader/#f%d' % feed.id)

@view(r'^opml/$', True)
def opml(request):
    feed_list = Feed.objects.all()
    response = render_to_response('reader/opml.xml', {'feed_list':feed_list})
    response['Content-Type'] = 'application/xml'
    response['Content-Disposition'] = 'attachment; filename=opml.xml'
    return response

