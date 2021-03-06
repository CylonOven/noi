# -*- coding: utf-8 -*-
# Copyright 2016 Luc Saffre
# License: BSD (see file COPYING for details)

"""Runs some tests about the disable-delete handler and cascading deletes.

You can run only these tests by issuing::

  $ go noi
  $ cd lino_noi/projects/care
  $ python manage.py test tests.test_cascaded_delete

Or::

  $ go noi
  $ python setup.py test -s tests.DemoTests.test_care

This tests for :ticket:`1177`, :ticket:`1180`, :ticket:`1181`

"""

from __future__ import unicode_literals
from __future__ import print_function
import six

from django.core.exceptions import ValidationError
from lino.utils.djangotest import RemoteAuthTestCase
from lino.api import rt


def create(m, **kwargs):
    obj = m(**kwargs)
    obj.full_clean()
    obj.save()
    return obj
    

class Tests(RemoteAuthTestCase):
    maxDiff = None

    def test01(self):
        from lino.modlib.users.choicelists import UserTypes
        User = rt.modules.users.User
        Faculty = rt.models.faculties.Faculty
        Competence = rt.models.faculties.Competence
        Ticket = rt.models.tickets.Ticket
        TicketStates = rt.actors.tickets.TicketStates

        general = create(Faculty, name="General work")
        special = create(Faculty, name="Special work", parent=general)

        alex = create(User, username='alex',
                       profile=UserTypes.user,
                       language="en")
        
        bruno = create(User, username='bruno',
                       profile=UserTypes.user,
                       language="en")
        
        berta = create(User, username='berta',
                       profile=UserTypes.user,
                       language="en")
        
        create(Competence, user=bruno, faculty=special)
        create(Competence, user=alex, faculty=general)
        
        ticket1 = create(
            Ticket, summary="Need general help",
            user=berta, faculty=general)

        ticket2 = create(
            Ticket, summary="Need special help",
            user=berta, faculty=special)

        self.assertEqual(ticket1.state, TicketStates.new)

        ar = rt.actors.faculties.AssignableWorkersByTicket.request(ticket1)
        s = ar.to_rst()
        # print(s)
        self.assertEquivalent("""
==========
 Username
----------
 alex
==========
""", s)


        ar = rt.actors.faculties.AssignableWorkersByTicket.request(ticket2)
        s = ar.to_rst()
        # print(s)
        self.assertEquivalent("""
==========
 Username
----------
 alex
 bruno
==========
""", s)


        # cannot delete a faculty when there are competences referring
        # to it:
        try:
            special.delete()
            self.fail("Expected veto")
        except Warning as e:
            self.assertEqual(
                six.text_type(e), "Cannot delete Faculty Special work "
                "because 1 Competences refer to it.")

        # you cannot delete a faculty when it is the parent of other
        # faculties
        try:
            general.delete()
            self.fail("Expected veto")
        except Warning as e:
            self.assertEqual(
                six.text_type(e), "Cannot delete Faculty General work "
                "because 1 Competences refer to it.")
            
        # deleting a user will automatically delete all their
        # competences:
        
        bruno.delete()
        alex.delete()

        self.assertEqual(Ticket.objects.count(), 2)

        # from lino.core.merge import MergePlan
        # mp = MergePlan(berta, None)
        # mp.analyze()
        # s = mp.logmsg()
        # print(s)
        # self.assertEqual(s, '')
        
        # Deleting a user who reported a ticket is not refused because
        # Ticket.user is nullable. The tickets won't be deleted,
        # but their `user` field will be set to NULL:

        if False:
        
            berta.delete()

            self.assertEqual(Ticket.objects.count(), 2)

            # ticket1 = Ticket.objects.get(pk=1)
            # ticket2 = Ticket.objects.get(pk=2)

            self.assertEqual(ticket1.user, None)
            self.assertEqual(ticket2.user, None)

        # make sure that database state is as expected:

        self.assertEqual(Faculty.objects.count(), 2)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(Ticket.objects.count(), 2)
        self.assertEqual(Competence.objects.count(), 0)
        
        
