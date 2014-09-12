# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from trytond.pool import Pool
from .work import *
from .contact_mechanism import *

def register():
    Pool.register(
        ContactMechanism,
        WorkAsteriskResult,
        module='project_asterisk', type_='model')
    Pool.register(
        WorkAsterisk,
        module='project_asterisk', type_='wizard')
