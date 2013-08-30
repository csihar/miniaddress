from django.core.management.base import BaseCommand, CommandError
from optparse import make_option
from miniaddress.models import House, Owner
from miniaddress.functions import check_existence

class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option('--addr-contains',
            action='store',
            type='string',
            dest='addr-contains',
            default='',
            help="Part of address of the house to delete"),
        )    
    
    def handle(self, *args, **options):
        ''' Delete address with --addr-contains=foo '''
        if options['addr-contains']:
            address = options['addr-contains']
            del_house = House.objects.filter(address__icontains=address)
            if not del_house:
                self.stdout.write('No houses containing [%s]' % address )
            for house in del_house:
                house_id = house.id
                address = house.address
                owner = house.owner
                house.delete()
                self.stdout.write('Deleted house: id=[%s] address=[%s] owner=[%s]\n' % (house_id, address, owner) )
                owner_has_house = House.objects.filter(owner__name=owner)
                if not owner_has_house:
                    del_owner = Owner.objects.get(name=owner)
                    del_owner.delete()
                    self.stdout.write('Deleted owner: name=[%s]\n' % owner )
        else:
            raise CommandError('Please specify an address')

