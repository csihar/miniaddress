from django.core.management.base import BaseCommand, CommandError
from optparse import make_option
from miniaddress.models import House


class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option('--owner',
            action='store',
            type='string',
            dest='house_owner',
            default='',
            help='Filter houses displayed by owner'),
        )
        
    def handle(self, *args, **options):
        ''' Show all houses.
            Limit to a specific owner with --owner=foo '''
        houses = House.objects.all()
        if options['house_owner']:
            house_owner = options['house_owner']
            try:
                houses = House.objects.filter(owner__name=house_owner)
            except House.DoesNotExist:
                raise CommandError('Owner [%s] does not exist' % house_owner )
        if houses:
            for house in houses:
                n = house.id
                address = house.address
                owner = house.owner
                self.stdout.write('id=[%s] address=[%s] owner=[%s]\n' % (n, address, owner) )
        else:
            raise CommandError('No houses to display')
