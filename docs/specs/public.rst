.. _noi.specs.public:

==========================
Public read-only interface
==========================

.. How to test only this document:

    $ python setup.py test -s tests.SpecsTests.test_public
    
    doctest init:

    >>> from __future__ import print_function 
    >>> from __future__ import unicode_literals
    >>> import os
    >>> os.environ['DJANGO_SETTINGS_MODULE'] = 'lino_noi.projects.bs3.settings.demo'
    >>> from lino.api.doctest import *


This document specifies the read-only public interface of Lino Noi.
implemented in :mod:`lino_noi.projects.public`.


.. contents::
  :local:

Public tickets
==============

This is currently the only table publicly available.

The demo database contains the following data:

>>> rt.show(tickets.PublicTickets)
... #doctest: +REPORT_UDIFF
================================== ======= ============= ========= =========== ==========
 Overview                           State   Ticket type   Project   Product     Priority
---------------------------------- ------- ------------- --------- ----------- ----------
 *#13 (Bar cannot foo)*             New     Bugfix        linö      Lino Cosi   0
 *#1 (Föö fails to bar when baz)*   New     Bugfix        linö      Lino Cosi   0
================================== ======= ============= ========= =========== ==========
<BLANKLINE>

This data is being rendered using plain bootstrap HTML:

>>> res = test_client.get('/')
>>> res.status_code
200
>>> soup = BeautifulSoup(res.content)
>>> links = soup.find_all('a')
>>> len(links)
29
>>> print(links[0].get('href'))
/?ul=de
>>> print(links[1].get('href'))
/?ul=fr
>>> print(links[2].get('href'))
#
>>> print(links[4].get('href'))
/tickets/Tickets

>>> res = test_client.get('/tickets/Tickets/7')
>>> res.status_code
200
>>> soup = BeautifulSoup(res.content)
>>> print(soup.get_text(' ', strip=True))
... #doctest: +NORMALIZE_WHITESPACE +REPORT_UDIFF +ELLIPSIS
Tickets Home en de fr Tickets Active tickets Tickets Site About #7 (No Foo after deleting Bar) << < > >> State: New
<BLANKLINE>
<BLANKLINE>
(last update ...) Reported by: Robin Rood ... Product: Lino Core Site: welket No dependencies. This is Lino Noi ...
