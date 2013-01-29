#!/usr/bin/python

#import settings
from django.core.management import setup_environ

setup_environ(settings)

from reader.models import Feed

def update_all():
    for feed in Feed.objects.all():
        try:
            feed.update()
        except:
            pass

def main():
    update_all()

if __name__ == "__main__":
    main()

