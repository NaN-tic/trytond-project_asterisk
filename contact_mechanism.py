#This file is part of project_asterisk module for Tryton.
#The COPYRIGHT file at the top level of this repository contains
#the full copyright notices and license terms.
from trytond.pool import PoolMeta

__all__ = ['ContactMechanism']


class ContactMechanism:
    __metaclass__ = PoolMeta
    __name__ = 'party.contact_mechanism'

    def get_rec_name(self, name):
        if self.party:
            return self.value + ' (' + self.party.get_rec_name(name) + ')'
        return super(ContactMechanism, self).get_rec_name(name)
