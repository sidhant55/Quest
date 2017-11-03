from django.core.management.base import BaseCommand, CommandError
from quests.models import user
import string
import random

class Command(BaseCommand):
    help = 'give params as name and email'

    """Function to accept parameter"""

    def add_arguments(self, parser):
        parser.add_argument('name', type=str)
        parser.add_argument('email', type=str)

    """Function to handle request"""

    def handle(self, *args, **options):

        name = options['name']

        #framing key
        key=''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10))+"^"+name

        var=user()
        var.name=name
        var.key=key
        var.email=options['email']

        #save data to database

        var.save()

        #display key to the user

        self.stdout.write(self.style.SUCCESS('Successfully closed poll %s'%key))