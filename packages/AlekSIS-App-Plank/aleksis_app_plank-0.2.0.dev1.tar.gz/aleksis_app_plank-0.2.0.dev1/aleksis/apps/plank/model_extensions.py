from aleksis.core.models import Person


@Person.method
def get_checked_out_items(self):
    checks = []
    for check_out in self.check_outs_as_borrowing.all():
        checks += check_out.checked_out_items.all()
    return checks
