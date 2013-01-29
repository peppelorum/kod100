import re
import datetime
import urllib2
import feedparser

from django.core.mail import mail_admins

from models import Post

def update_feeds(feed):
    feed.error = None
    guid = None
    dtMax = feed.dt_updated
    dtMod = None
    if feed.dt_updated and (datetime.datetime.now() - feed.dt_updated).days < 30:
        dtMod = feed.dt_updated.timetuple()
    try:
        d = feedparser.parse(feed.feed_url, modified=dtMod)
    except urllib2.URLError, e:
        mail_admins("URLError in updating %s" % feed, "%s\n%s\n\n%s" % (feed, feed.feed_url, e))
        print feed, feed.feed_url
        print e
        return
    if d.get('status', 200) in (200, 307):
        Post.objects.filter(feed=feed).update(current=False)
        for entry in d.entries:
            try:
                dt = datetime.datetime.now()
                if entry.has_key('updated_parsed') and entry.updated_parsed:
                    dt = datetime.datetime(*entry.updated_parsed[:6])
                content = entry.get('content', [{'value':''}])[0]['value']
                description = entry.get('description', '')
                if len(description) > len(content):
                    content = description
                title = entry.get('title', 'Untitled')
                author = entry.get('author','Anonymous')
                link = entry.link
                guid = entry.get('guid', None)
                if not guid:
                    guid = link
                exclude = False
                for filter in feed.filters.all():
                    to_filter = ''
                    if filter.filter_on == FILTER_ON_CHOICES.Title:
                        to_filter = title
                    elif filter.filter_on == FILTER_ON_CHOICES.Body:
                        to_filter = content
                    flags = re.IGNORECASE if filter.ignore_case else 0
                    exclude = exclude or re.search(filter.regex, to_filter, flags)
                if not exclude:
                    post, created = Post.objects.get_or_create(
                                        guid=guid, feed=feed,
                                        defaults={'dt_published':dt,
                                                    'title':title,
                                                    'author':author,
                                                    'content':content,
                                                    'link':link})
                    dtMax = max(dtMax, post.dt_published)
                    post.current = True
                    post.save()
            except Exception, e:
                mail_admins("Error in updating %s" % feed, "%s\n%s\n\n%s" % (feed, guid, e))
                print feed, guid
                print e
                return
    elif d.status in (301, 302, 303):
        feed.feed_url = d.get('href', feed.feed_url)
    elif d.status in (304,):
        pass
    else:
        feed.error = int(d.status)
    Post.objects.filter(feed=feed, dt_cached__lt=(datetime.datetime.now()-datetime.timedelta(30))).update(content='')
    feed.dt_checked = datetime.datetime.now()
    feed.dt_updated = dtMax
    feed.save()

