# -*- coding: UTF-8 -*-
# Copyright 2016 Luc Saffre
#
# License: BSD (see file COPYING for details)
"""The default :attr:`workflows_module
<lino.core.site.Site.workflows_module>` for :ref:`noi` applications.

This workflow requires that both :mod:`lino_noi.lib.tickets` and
:mod:`lino_noi.lib.votes` are installed.

If :attr:`use_new_unicode_symbols
<lino.core.site.Site.use_new_unicode_symbols>` is True, ticket states
are represented using symbols from the `Miscellaneous Symbols and
Pictographs
<https://en.wikipedia.org/wiki/Miscellaneous_Symbols_and_Pictographs>`__
block, otherwise we use the more widely supported symbols from
`Miscellaneous Symbols
<https://en.wikipedia.org/wiki/Miscellaneous_Symbols>`
`fileformat.info
<http://www.fileformat.info/info/unicode/block/miscellaneous_symbols/list.htm>`__.

"""
from __future__ import unicode_literals

from lino.api import dd, _, pgettext
from django.conf import settings

from lino_noi.lib.tickets.choicelists import TicketStates
from lino_noi.lib.tickets.roles import Triager
from lino_noi.lib.votes.choicelists import VoteStates #, VoteViews
from lino.modlib.notify.actions import NotifyingAction

"""
"""

add = TicketStates.add_item

# add('10', _("Assigned"), 'assigned',
#     required=dict(states=['', 'active']),
#     action_name=_("Start"),
#     help_text=_("Ticket has been assigned to somebody who is assigned on it."))
add('10', _("New"), 'new', active=True, show_in_todo=True)
add('15', _("Talk"), 'talk', active=True)
add('20', _("Opened"), 'opened', active=True, show_in_todo=True)
add('21', _("Sticky"), 'sticky', active=True)
add('22', _("Started"), 'started', active=True, show_in_todo=True)
add('30', _("Sleeping"), 'sleeping')
add('40', _("Ready"), 'ready', active=True)
add('50', _("Closed"), 'closed')
add('60', _("Cancelled"), 'cancelled')
# TicketStates.default_value = 'new'

if settings.SITE.use_new_unicode_symbols:

    TicketStates.new.button_text =u"📥"  # INBOX TRAY (U+1F4E5)
    TicketStates.talk.button_text =u"🗪"  # TWO SPEECH BUBBLES (U+1F5EA)
    TicketStates.opened.button_text = u"☉"  # SUN (U+2609)	
    TicketStates.started.button_text=u"🐜"  # ANT (U+1F41C)
    TicketStates.cancelled.button_text=u"🗑"  # WASTEBASKET (U+1F5D1)
    TicketStates.sticky.button_text=u"📌"  # PUSHPIN (U+1F4CC)
    TicketStates.sleeping.button_text = u"🕸"  # SPIDER WEB (U+1F578)	
    TicketStates.ready.button_text = "\u2610"  # BALLOT BOX
    TicketStates.closed.button_text = "\u2611"  # BALLOT BOX WITH CHECK

else:    
    TicketStates.new.button_text ="⛶"  # SQUARE FOUR CORNERS (U+26F6)
    # TicketStates.talk.button_text = "⚔"  # CROSSED SWORDS (U+2694)
    TicketStates.talk.button_text = "☎"  # Black Telephone (U+260E)
    TicketStates.opened.button_text = "☉"  # SUN (U+2609)	
    # TicketStates.started.button_text="☭"  # HAMMER AND SICKLE (U+262D)
    TicketStates.started.button_text = "⚒"  # HAMMER AND PICK (U+2692
    # TicketStates.sticky.button_text="♥"  # BLACK HEART SUIT (U+2665)
    TicketStates.sticky.button_text="♾"  # (U+267E)
    TicketStates.sleeping.button_text = "☾"  # LAST QUARTER MOON (U+263E)
    TicketStates.ready.button_text = "☐"  # BALLOT BOX \u2610
    TicketStates.closed.button_text = "☑"  # BALLOT BOX WITH CHECK \u2611
    TicketStates.cancelled.button_text="☒"  # BALLOT BOX WITH X (U+2612)

class TicketAction(dd.ChangeStateAction):
    """Base class for ticket actions.

    Make sure that only *triagers* can act on tickets of other users.

    """
    def get_action_permission(self, ar, obj, state):
        me = ar.get_user()
        if obj.user != me:
            if not me.profile.has_required_roles([Triager]):
                return False
        return super(TicketAction,
                     self).get_action_permission(ar, obj, state)

# class NotifyingTicketAction(TicketAction):
    
#     def get_notify_owner(self, ar, obj):
#         return obj

#     def get_notify_recipients(self, ar, obj):
#         yield obj.get_notify_recipients(ar)

    
class MarkTicketOpened(TicketAction):
    """Mark this ticket as open.
    """
    label = pgettext("verb", "Open")
    required_states = 'talk new closed'
    show_in_bbar = True

    # def get_notify_subject(self, ar, obj):
    #     subject = _("{user} opened {ticket}.").format(
    #         user=ar.get_user(), ticket=obj)
    #     return subject
    
    
class MarkTicketStarted(TicketAction):
    """Mark this ticket as started.
    """
    label = pgettext("verb", "Start")
    required_states = 'talk opened'

    # def get_notify_subject(self, ar, obj):
    #     subject = _("{user} activated {ticket}.").format(
    #         user=ar.get_user(), ticket=obj)
    #     return subject
    
class MarkTicketReady(TicketAction):
    """Mark this ticket as ready.
    """
    required_states = "new opened started talk"
    
class MarkTicketClosed(TicketAction):
    """Mark this ticket as closed.
    """
    label = pgettext("verb", "Close")
    required_states = 'talk started opened ready'


class MarkTicketTalk(TicketAction):
    """Mark this ticket as talk.
    """
    label = pgettext("verb", "Talk")
    required_states = "new opened started sleeping ready"

    # def get_notify_subject(self, ar, obj):
    #     subject = _("{user} wants to talk about {ticket}.").format(
    #         user=ar.get_user(), ticket=obj)
    #     return subject


TicketStates.sticky.add_transition(
    required_states="new")
TicketStates.new.add_transition(
    required_states="sticky")
TicketStates.sleeping.add_transition(
    required_states="new talk opened started")
TicketStates.talk.add_transition(MarkTicketTalk)
TicketStates.opened.add_transition(MarkTicketOpened)
TicketStates.started.add_transition(MarkTicketStarted)
TicketStates.ready.add_transition(MarkTicketReady)
TicketStates.closed.add_transition(MarkTicketClosed)


add = VoteStates.add_item
add('10', _("Watching"), _("Interest"), 'watching')
add('20', _("Candidate"), _("Offer"), 'candidate', show_in_todo=True)
add('30', _("Assigned"), _("Job to do"), 'assigned', show_in_todo=True)
add('40', _("Done"), _("Job done"), 'done')
add('50', _("Rated"), _("Job rated"), 'rated')
add('60', _("Cancelled"), _("Cancelled offer"), 'cancelled')  # Absage


# add = VoteViews.add_item
# add('10', _("Offers"), 'offers', show_states=set([
#     VoteStates.candidate]))
# add('20', _("Tasks"), 'tasks', show_states=set([
#     VoteStates.assigned, VoteStates.done]))


# VoteStates.default_value = 'watching'
# VoteStates.offers_states = 
# VoteStates.tasks_states = 


class VoteAction(dd.ChangeStateAction, NotifyingAction):
    
    managed_by_votable_author = False
    msg_template = _("{user} marked {vote} as {state}.")
    
    def get_notify_subject(self, ar, obj):
        subject = _(self.msg_template).format(
            user=ar.get_user(),
            voter=obj.user,
            vote=obj,
            state=obj.state,
            ticket=obj.votable)
        return subject
    
    def get_notify_owner(self, ar, obj):
        return obj.votable.get_notify_owner(ar, obj)

    def get_notify_recipients(self, ar, obj):
        yield obj.votable.get_notify_recipients(ar)

    def get_action_permission(self, ar, obj, state):
        me = ar.get_user()
        if self.managed_by_votable_author:
            mgr = obj.votable.user
        else:
            mgr = obj.user
        if mgr != me:
            if not me.profile.has_required_roles([Triager]):
                return False
        return super(VoteAction,
                     self).get_action_permission(ar, obj, state)

class MarkVoteAssigned(VoteAction):
    
    label = pgettext("verb", "Assign")
    managed_by_votable_author = True
    required_states = 'candidate'
    msg_template = _("{user} assigned {voter} for {ticket}.")


class MarkVoteCancelled(VoteAction):
    
    label = pgettext("verb", "Cancel")
    managed_by_votable_author = True
    required_states = 'candidate assigned'
    msg_template = _("{user} cancelled {vote} for {ticket}.")


class MarkVoteDone(VoteAction):
    
    label = _("Done")
    managed_by_votable_author = False
    required_states = 'assigned'
    msg_template = _("{user} confirmed {ticket} {state} by {voter}.")

    
class MarkVoteCandidate(VoteAction):
    
    label = _("Candidate")
    managed_by_votable_author = False
    msg_template = _("{user} candidates for {ticket}.")
    required_states = "watching open"
    

class MarkVoteCandidate(VoteAction):
    
    label = _("Candidate")
    managed_by_votable_author = False
    msg_template = _("{user} candidates for {ticket}.")
    required_states = "watching"
    

class MarkVoteRated(VoteAction):
    """Mark this vote as rated."""
    label = _("Rated")
    managed_by_votable_author = True
    required_states = 'assigned done'
    
    def get_action_permission(self, ar, obj, state):
        if not obj.rating:
            return False
        return super(MarkVoteRated,
                     self).get_action_permission(ar, obj, state)



VoteStates.watching.add_transition(
    required_states="candidate assigned")
VoteStates.candidate.add_transition(MarkVoteCandidate)
VoteStates.assigned.add_transition(MarkVoteAssigned)
VoteStates.done.add_transition(MarkVoteDone)
VoteStates.rated.add_transition(MarkVoteRated)
VoteStates.cancelled.add_transition(MarkVoteCancelled)



# TicketStates.favorite_states = (TicketStates.sticky, )
# TicketStates.work_states = (TicketStates.todo, TicketStates.new)
# TicketStates.waiting_states = (TicketStates.done, )

