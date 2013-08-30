from django.core.management.base import BaseCommand, CommandError
from optparse import make_option
from miniaddress.models import House, Owner
from miniaddress.functions import check_existence

class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option('--id',
            action='store',
            type='int',
            dest='house_id',
            default=0,
            help="Specify id of house to modify"),
        ) + (
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
        ''' Specify id of house to modify with --id=foo
            Change address with --address=bar 
            Change owner with --owner=baz '''

        if options['house_id']:
            house_id = options['house_id']
            try:
                house_to_modify = House.objects.get(id=house_id)
            except House.DoesNotExist:
                raise CommandError('No house with id=[%s]' % house_id )

            if options['owner']:
                modified_owner = options['owner']
                owner_exists = check_existence('owner', modified_owner)
                if not owner_exists:
                    new_owner = Owner(name=modified_owner)
                    new_owner.save()
                    self.stdout.write('Added owner: name=[%s]\n' % modified_owner)
                new_owner = Owner.objects.get(name=modified_owner)
                house_to_modify.owner = new_owner
                house_to_modify.save()
                self.stdout.write('Modified owner: id=[%s] name=[%s] address=[%s]\n' % (house_id, house_to_modify.owner, house_to_modify.address) )
                                
            if options['address']:
                modified_address = options['address']
                house_to_modify.address = modified_address
                house_to_modify.save()
                self.stdout.write('Modified address: id=[%s] address=[%s] owner=[%s]' % (house_id, house_to_modify.address, house_to_modify.owner) )

            if not options['address'] and not options['owner']:
                raise CommandError('Please specify an address or owner to modify')
        else:
            raise CommandError('Please specify the id of the house to be modified')
