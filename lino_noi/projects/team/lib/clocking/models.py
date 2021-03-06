# -*- coding: UTF-8 -*-
# Copyright 2016 Luc Saffre
# License: BSD (see file COPYING for details)

"""Database models for lino_noi.projects.team.lib.clocking.


"""

from lino_noi.lib.clocking.models import *
from lino.api import _
from lino.mixins.periods import DatePeriod
from lino_xl.lib.excerpts.mixins import Certifiable
from lino_noi.lib.tickets.choicelists import TicketStates


dd.inject_field(
    "users.User", 'open_session_on_new_ticket',
    models.BooleanField(_("Open session on new ticket"), default=False))


class ServiceReport(UserAuthored, Certifiable, DatePeriod):
    """A **service report** is a document used in various discussions with
    a stakeholder.

    .. attribute:: user

        This can be empty and will then show the working time of all
        users.


    .. attribute:: start_date
    .. attribute:: end_date
    .. attribute:: interesting_for
    .. attribute:: ticket_state

    .. attribute:: printed
        See :attr:`lino.modlib.exerpts.mixins.Certifiable.printed`

    """
    class Meta:
        verbose_name = _("Service Report")
        verbose_name_plural = _("Service Reports")

    interesting_for = dd.ForeignKey(
        'contacts.Partner',
        verbose_name=_("Interesting for"),
        blank=True, null=True,
        help_text=_("Only tickets interesting for this partner."))

    ticket_state = TicketStates.field(
        null=True, blank=True,
        help_text=_("Only tickets in this state."))

    def get_tickets_parameters(self, **pv):
        """Return a dict with parameter values for `tickets.Tickets` based on
        the options of this report.

        """
        pv.update(start_date=self.start_date, end_date=self.end_date)
        pv.update(interesting_for=self.interesting_for)
        if self.ticket_state:
            pv.update(state=self.ticket_state)
        return pv
        


from .ui import *
