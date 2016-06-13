.. _noi.specs.bs3:

=====================================================
A read-only interface to Team using generic Bootstrap
=====================================================

.. How to test only this document:

    $ python setup.py test -s tests.SpecsTests.test_bs3
    
    doctest init:

    >>> from lino import startup
    >>> startup('lino_noi.projects.bs3.settings.demo')
    >>> from lino.api.doctest import *


This document specifies the read-only public interface of Lino Noi.
implemented in :mod:`lino_noi.projects.bs3`.

Provides readonly anonymous access to the data of
:mod:`lino_noi.projects.team`, using the :mod:`lino.modlib.bootstrap3`
user interface. See also :mod:`lino_noi.projects.public`

This does not use :mod:`lino.modlib.extjs` at all.


.. contents::
  :local:

.. The following was used to reproduce :ticket:`960`:

    >>> res = test_client.get('/tickets/Ticket/13')
    >>> res.status_code
    200



Unassigned tickets
==================


The demo database contains the following data:

>>> rt.show(tickets.PublicTickets)
... #doctest: +REPORT_UDIFF
================================== ======= ============= ========= =========== ==========
 Overview                           State   Ticket type   Project   Topic       Priority
---------------------------------- ------- ------------- --------- ----------- ----------
 *#13 (Bar cannot foo)*             Done    Bugfix        linö      Lino Cosi   0
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

>>> res = test_client.get('/tickets/Ticket/13')
>>> res.status_code
200
>>> soup = BeautifulSoup(res.content)


>>> links = soup.find_all('a')
>>> len(links)
31
>>> print(links[0].get('href'))
/?ul=en

>>> print(soup.get_text(' ', strip=True))
... #doctest: +NORMALIZE_WHITESPACE +REPORT_UDIFF +ELLIPSIS
Tickets Home en de fr Tickets Active tickets Tickets Unassigned Tickets Site About #13 (Bar cannot foo) << < > >> State: Done  
<BLANKLINE>
<BLANKLINE>
(last update ...) Reported by: Rolf Rompen ... Topic: Lino Cosi Site: welket Linking to #1 and to blog . This is Lino Noi 1.0.1 using Lino 1.7.0, Django 1.9.6, Python 2.7.6, Babel 2.2.0, Jinja 2.8, Sphinx 1.4a1, python-dateutil 2.5.2, OdfPy ODFPY/1.3.2, docutils 0.12, suds 0.4, PyYaml 3.11, Appy 0.9.2 (2015/04/30 15:00), Bootstrap 3.3.4, TinyMCE 3.5.11, Ext.ux.TinyMCE 0.8.4