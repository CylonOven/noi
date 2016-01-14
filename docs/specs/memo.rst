.. _noi.specs.memo:

=============
Memo commands
=============

.. How to test only this document:

    $ python setup.py test -s tests.SpecsTests.test_memo
    
    doctest init:

    >>> from __future__ import print_function 
    >>> from __future__ import unicode_literals
    >>> from lino import startup
    >>> startup('lino_noi.projects.team.settings.demo')
    >>> from lino.api.doctest import *
    >>> rt.startup()
    >>> ses = rt.login(renderer=dd.plugins.extjs.renderer)

The :attr:`description
<lino_noi.lib.tickets.models.Ticket.description>` of a ticket is a
formatted HTML text which can contain links, tables, headers, enumerations...

... and it can additionally contain :mod:`memo <lino.utils.memo>`
markup. Examples:

url
===

Insert a link to an external web page. The first argument is the URL
(mandatory). If no other argument is given, the URL is used as
text. Otherwise the remaining text is used as the link text

Usage examples:

- ``[url http://www.example.com]``
- ``[url http://www.example.com example]``

..  test:
    >>> print(ses.parse_memo("See also [url http://www.example.com]."))
    See also <a href="http://www.example.com">http://www.example.com</a>.
    >>> print(ses.parse_memo("See also [url http://www.example.com example]."))
    See also <a href="http://www.example.com">example</a>.


ticket
======

Refer to a ticket. Usage example: 

  See ``[ticket 1]``.

Note that the current renderer decides how to render the link. For
example, the default user interface :mod:`lino.modlib.extjs` will
render it like this:

>>> ses = rt.login(renderer=dd.plugins.extjs.renderer)
>>> print(ses.parse_memo("See [ticket 1]."))
See <a href="javascript:Lino.tickets.Tickets.detail.run(null,{ &quot;record_id&quot;: 1 })" title="F&#246;&#246; fails to bar when baz">#1</a>.

While the :mod:`lino.modlib.bootstrap3` user interface will render it
like this:

>>> ses = rt.login(renderer=dd.plugins.bootstrap3.renderer)
>>> print(ses.parse_memo("See [ticket 1]."))
See <a href="/bs3/tickets/Ticket/1" title="F&#246;&#246; fails to bar when baz">#1</a>.

Or the plain text renderer will render:

>>> ses = rt.login()
>>> print(ses.parse_memo("See [ticket 1]."))
See <em>#1</em>.