from miniaddress.models import House, Owner


def check_existence(mode, subject):
    exists=True
    if mode == "house":
        try:
            house = House.objects.get(address=subject)
        except House.DoesNotExist:
            exists = False
        return exists
    if mode == "owner":
        try:
            owner = Owner.objects.get(name=subject)
        except Owner.DoesNotExist:
            exists = False
        return exists