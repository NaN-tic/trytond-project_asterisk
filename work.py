#This file is part of project_asterisk module for Tryton.
#The COPYRIGHT file at the top level of this repository contains
#the full copyright notices and license terms.
from trytond.model import ModelView, fields
from trytond.pool import Pool
from trytond.transaction import Transaction
from trytond.pyson import Eval
from trytond.wizard import Wizard, StateView, StateTransition, Button

__all__ = ['WorkAsteriskResult', 'WorkAsterisk']


class WorkAsteriskResult(ModelView):
    'Work Asterisk Result'
    __name__ = 'project.work.asterisk.result'

    phone = fields.Selection('get_phones', 'Phone', required=True)
    allowed_contacts_mechanisms = fields.Function(fields.One2Many(
            'party.contact_mechanism', None, 'Allowed Contacts Mechanisms'),
        'on_change_with_allowed_contacts_mechanisms')
    contact_mechanisms = fields.Many2One('party.contact_mechanism',
        'Contact Mechanisms',
        domain=[
            ('id', 'in', Eval('allowed_contacts_mechanisms', [])),
            ],
        depends=['allowed_contacts_mechanisms'])


class WorkAsterisk(Wizard):
    'Work Asterisk'
    __name__ = 'project.work.asterisk'

    start = StateView('project.work.asterisk.result',
        'project_asterisk.work_asterisk_result_view_form', [
            Button('Cancel', 'end', 'tryton-cancel'),
            Button('Dial', 'dial', 'tryton-ok', default=True),
            ])
    dial = StateTransition()

    def get_mechanims(self, party):
        mechanisms = []
        for mechanism in party.contact_mechanisms:
            if mechanism.type in ('phone', 'mobile'):
                mechanisms.append(mechanism)
        if party.relations:
            for relationship in party.relations:
                for mechanism in relationship.to.contact_mechanisms:
                    if mechanism.type in ('phone', 'mobile'):
                        mechanisms.append(mechanism)
        return mechanisms

    def default_start(self, fields):
        """
        This method searches phones of the activities in a project/task to
        show in the wizard.
        """
        Work = Pool().get('project.work')
        work = Transaction().context.get('active_id')
        if work:
            work = Work(work)
            mechanisms = []
            for activity in work.activities:
                if activity.contacts:
                    mechanisms.extend(self.get_mechanims(activity.contacts[0]))
                for contact in activity.contacts:
                    mechanisms.extend(self.get_mechanims(contact))
        mechanisms = list(set(mechanisms))
        return {
            'allowed_contacts_mechanisms': [m.id for m in mechanisms],
            'contact_mechanisms': mechanisms and mechanisms[0].id or None
            }

    def transition_dial(self, values=False):
        """
        Function called by the button 'Dial'
        """
        party = self.start.contact_mechanisms.party
        number = self.start.contact_mechanisms.value
        Asterisk = Pool().get('asterisk.configuration')
        Asterisk.dial(party, number)
        return 'end'
