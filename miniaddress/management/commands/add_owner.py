from django.core.management.base import BaseCommand, CommandError
from optparse import make_option
from miniaddress.models import Owner
from miniaddress.functions import check_existence


class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option('--name',
            action='store',
            type='string',
            dest='name',
            default='',
            help="Specify owner's name"),
        )
        
    def handle(self, *args, **options):
        ''' Add owner with --name=foo '''
        if options['name']:
            name = options['name']
            owner_exists = check_existence('owner', name)
            if owner_exists:
                self.stdout.write('Owner [%s] already exists' % name )
            else:
                new_owner = Owner(name=name)
                new_owner.save()
                self.stdout.write('Added owner: name=[%s]' % name)
        else:
            raise CommandError('Please specify a name')
