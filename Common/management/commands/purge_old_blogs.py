import datetime
from django.core.management.base import BaseCommand

from BlogControl.models import Blog, Comment


class Command(BaseCommand):
    help = 'Purge blogs older than a year'

    def handle(self, *args, **options):
        timedelta = datetime.timedelta(days=-365)
        end_date = datetime.datetime.now() + timedelta

        for blog in Blog.objects.filter(date_created__lte=end_date):
            for comment in Comment.objects.filter(blog=blog):
                comment.delete()
                pass
            print "Deleting Blog %s" % blog.slug
            blog.delete()

        self.stdout.write(self.style.SUCCESS('Successfully purged old blogs' ))