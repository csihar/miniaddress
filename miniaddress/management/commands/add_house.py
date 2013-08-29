from django.core.management.base import BaseCommand, CommandError
from optparse import make_option
from miniaddress.models import House, Owner
from miniaddress.functions import check_existence

class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option('--address',
            action='store',
            type='string',
            dest='address',
            default='',
            help="Specify house's address"),
        ) + (
        make_option('--owner',
            action='store',
            type='string',
            dest='owner',
            default='',
            help="Specify house's owner"),
        )
    
    
    def handle(self, *args, **options):
        ''' Add address with --address=foo 
            Specify owner with --owner=bar '''

        if options['owner']:
            owner = options['owner']
            owner_exists = check_existence('owner', owner)
            if not owner_exists:
                new_owner = Owner(name=owner)
                new_owner.save()
                self.stdout.write('Added owner: name=[%s]\n' % owner)
        else:
            raise CommandError('Please specify an owner')
            
            
        if options['address']:
            address = options['address']
            house_exists = check_existence('house', address)
            if house_exists:
                self.stdout.write('House at [%s] already exists' % address )
            else:
                owner_inst = Owner.objects.get(name=owner)
                new_house = House(address=address, owner=owner_inst)
                new_house.save()
                self.stdout.write('Added house: address=[%s] owner=[%s]' % (address, owner) )
        else:
            raise CommandError('Please specify an address')

