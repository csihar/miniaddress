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
        ) + (
        make_option('--addr-contains',
            action='store',
            type='string',
            dest='addr-contains',
            default='',
            help="Part of address of the houses to show"),
        )    
        
    def handle(self, *args, **options):
        ''' Show all houses.
            Limit to a specific owner with --owner=foo
            Find address containing string "bar" with --addr-contains=bar '''
        houses = House.objects.all()

        if options['house_owner']:
            house_owner = options['house_owner']
            houses = houses.filter(owner__name=house_owner)
            if not houses:
                raise CommandError('Owner [%s] does not exist' % house_owner )

        if options['addr-contains']:
            addr_contains = options['addr-contains']
            houses = houses.filter(address__icontains=addr_contains)
            if not houses:
                raise CommandError('No houses with address containing [%s]' % addr_contains )

        if houses:
            for house in houses:
                n = house.id
                address = house.address
                owner = house.owner
                self.stdout.write('id=[%s] address=[%s] owner=[%s]\n' % (n, address, owner) )
        else:
            raise CommandError('No houses to display')
