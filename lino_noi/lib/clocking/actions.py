# -*- coding: UTF-8 -*-
# Copyright 2016 Luc Saffre
# License: BSD (see file COPYING for details)
"""Defines actions for this plugin."""


from django.db import models
from django.utils import timezone

from lino.api import dd, rt, _

from lino.mixins.periods import Monthly
from lino.modlib.printing.mixins import DirectPrintAction
from lino.core.roles import SiteUser
from .roles import Worker
from lino_noi.lib.tickets.roles import Triager

class EndSession(dd.Action):
    """Close a given session, i.e. stop working on that ticket for this
    time.  Common base for :class:`EndThisSession` and
    :class:`EndTicketSession`.

    """
    label = u"■"  # BLACK SQUARE (U+25A0)
    # label = u"◉"  # FISHEYE (U+25C9)
    # label = u"↘"  # u"\u2198"
    # label = _("End session")
    # label = u"\u231a\u2198"
    show_in_workflow = True
    show_in_bbar = False
    readonly = False
    required_roles = dd.required(Worker)

class EndThisSession(EndSession):
    """Close this session, i.e. stop working on that ticket for this time.

    """

    def get_action_permission(self, ar, obj, state):
        if obj.end_time:
            return False
        return super(EndThisSession, self).get_action_permission(ar, obj, state)

    def run_from_ui(self, ar, **kw):

        def ok(ar2):
            now = timezone.now()
            for obj in ar.selected_rows:
                obj.set_datetime('end', now)
                # obj.end_date = dd.today()
                # obj.end_time = now.time()
                obj.save()
                obj.ticket.touch()
                obj.ticket.save()
                ar2.set_response(refresh=True)

        if True:
            ok(ar)
        else:
            msg = _("Close {0} sessions.").format(len(ar.selected_rows))
            ar.confirm(ok, msg, _("Are you sure?"))


class EndTicketSession(EndSession):
    """End your running session on this ticket. 
    """
    
    def get_action_permission(self, ar, obj, state):
        # u = ar.get_user()
        # if not u.profile.has_required_roles([SiteUser]):
        #     # avoid query with AnonymousUser
        #     return False
        if not super(EndTicketSession, self).get_action_permission(
                ar, obj, state):
            return False
        user = ar.get_user()
            
        Session = rt.modules.clocking.Session
        qs = Session.objects.filter(
            user=user, ticket=obj, end_time__isnull=True)
        if qs.count() == 0:
            return False
        return True

    def run_from_ui(self, ar, **kw):
        Session = rt.modules.clocking.Session
        ses = Session.objects.get(
            user=ar.get_user(), ticket=ar.selected_rows[0],
            end_time__isnull=True)
        ses.set_datetime('end', timezone.now())
        ses.full_clean()
        ses.save()
        ar.set_response(refresh=True)


class StartTicketSession(dd.Action):
    """Start a session on this ticket."""
    # label = _("Start session")
    # label = u"\u262d"
    # label = u"\u2692"
    # label = u"\u2690"
    # label = u"\u2328"
    # label = u"\u231a\u2197"
    # label = u"↗"  # \u2197
    label = u"▶"  # BLACK RIGHT-POINTING TRIANGLE (U+25B6)
    # icon_name = 'emoticon_smile'
    show_in_workflow = True
    show_in_bbar = False
    readonly = True
    required_roles = dd.required(Worker)

    def get_action_permission(self, ar, obj, state):
        user = ar.get_user()
        if not obj.is_workable_for(user):
            return False
        if not super(StartTicketSession, self).get_action_permission(
                ar, obj, state):
            return False
        Session = rt.modules.clocking.Session
        qs = Session.objects.filter(
            user=user, ticket=obj, end_time__isnull=True)
        if qs.count():
            return False
        return True

    def run_from_ui(self, ar, **kw):
        me = ar.get_user()
        obj = ar.selected_rows[0]

        ses = rt.modules.clocking.Session(ticket=obj, user=me)
        ses.full_clean()
        ses.save()
        ar.set_response(refresh=True)

        


if dd.is_installed('clocking'):  # Sphinx autodoc
    dd.inject_action(
        dd.plugins.clocking.ticket_model,
        start_session=StartTicketSession())
    dd.inject_action(
        dd.plugins.clocking.ticket_model,
        end_session=EndTicketSession())


class PrintActivityReport(DirectPrintAction):
    """Print an activity report.

    Not yet used. This is meant to be used as a list action on
    Session, but Lino does not yet support list actions with a
    parameter window.

    """
    select_rows = False
    # combo_group = "creacert"
    label = _("Activity report")
    tplname = "activity_report"
    build_method = "weasy2html"
    icon_name = None
    parameters = Monthly(
        show_remarks=models.BooleanField(
            _("Show remarks"), default=False),
        show_states=models.BooleanField(
            _("Show states"), default=True))
    params_layout = """
    start_date
    end_date
    show_remarks
    show_states
    """
    keep_user_values = True
    # default_format = 'json'
    # http_method = 'POST'
