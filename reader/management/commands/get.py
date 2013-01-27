from django.core.management.base import BaseCommand, CommandError

from reader.models import Feed


class Command(BaseCommand):

    def handle(self, *args, **options):

        for feed in Feed.objects.all():
#            try:
            print 'yay', feed
            feed.update()
#            except:
#                print 'no', feed
#                pass

#
##!/usr/bin/python
#
##import settings
#from django.core.management import setup_environ
#
#setup_environ(settings)
#
#
#
#def update_all():
#
#
#def main():
#    update_all()
#
#if __name__ == "__main__":
#    main()
#
