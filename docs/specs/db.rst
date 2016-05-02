.. _noi.specs.db:

======================
The database structure
======================

.. To run only this test::

    $ python setup.py test -s tests.SpecsTests.test_db

    doctest init:

    >>> import lino
    >>> lino.startup('lino_noi.projects.team.settings.doctests')
    >>> from lino.api.doctest import *

This document describes the database structure.

>>> from lino.utils.diag import analyzer
>>> print(analyzer.show_db_overview())
... #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE +REPORT_UDIFF
32 apps: lino_startup, staticfiles, about, extjs, jinja, bootstrap3, printing, system, contenttypes, gfks, users, office, countries, contacts, products, notifier, changes, stars, uploads, outbox, excerpts, comments, tickets, faculties, clocking, lists, export_excel, tinymce, smtpd, appypod, wkhtmltopdf, noi.
44 models:
=========================== ============================ ========= =======
 Name                        Default table                #fields   #rows
--------------------------- ---------------------------- --------- -------
 changes.Change              changes.Changes              9         0
 clocking.ServiceReport      clocking.ServiceReports      7         1
 clocking.Session            clocking.Sessions            12        17
 clocking.SessionType        clocking.SessionTypes        4         1
 comments.Comment            comments.Comments            8         0
 contacts.Company            contacts.Companies           22        0
 contacts.CompanyType        contacts.CompanyTypes        7         0
 contacts.Partner            contacts.Partners            19        0
 contacts.Person             contacts.Persons             26        0
 contacts.Role               contacts.Roles               4         0
 contacts.RoleType           contacts.RoleTypes           4         0
 contenttypes.ContentType    gfks.ContentTypes            3         45
 countries.Country           countries.Countries          6         8
 countries.Place             countries.Places             8         78
 excerpts.Excerpt            excerpts.Excerpts            12        2
 excerpts.ExcerptType        excerpts.ExcerptTypes        17        2
 faculties.Competence        faculties.Competences        6         18
 faculties.Faculty           faculties.Faculties          9         8
 gfks.HelpText               gfks.HelpTexts               4         1
 lists.List                  lists.Lists                  7         8
 lists.ListType              lists.ListTypes              4         3
 lists.Member                lists.Members                5         0
 notifier.Notification       notifier.Notifications       7         0
 outbox.Attachment           outbox.Attachments           4         0
 outbox.Mail                 outbox.Mails                 9         0
 outbox.Recipient            outbox.Recipients            6         0
 products.Product            products.Products            9         4
 products.ProductCat         products.ProductCats         5         0
 stars.Star                  stars.Stars                  5         0
 system.SiteConfig           system.SiteConfigs           5         0
 tickets.Deployment          tickets.Deployments          4         0
 tickets.Interest            tickets.Interests            3         6
 tickets.Link                tickets.Links                4         1
 tickets.Milestone           tickets.Milestones           9         8
 tickets.Project             tickets.Projects             15        5
 tickets.ProjectType         tickets.ProjectTypes         4         0
 tickets.Site                tickets.Sites                4         3
 tickets.Ticket              tickets.Tickets              26        16
 tickets.TicketType          tickets.TicketTypes          4         3
 tinymce.TextFieldTemplate   tinymce.TextFieldTemplates   5         2
 uploads.Upload              uploads.Uploads              9         0
 uploads.UploadType          uploads.UploadTypes          8         0
 users.Authority             users.Authorities            3         0
 users.User                  users.Users                  16        7
=========================== ============================ ========= =======
<BLANKLINE>


Menus
-----

System administrator
--------------------

Rolf is a system administrator, he has a complete menu.

>>> ses = rt.login('robin') 
>>> ses.user.profile
users.UserProfiles.admin:900

>>> ses.show_menu()
... #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE +REPORT_UDIFF
- Contacts : Persons, Organizations, Partners, Partner Lists
- Products : Products, Product Categories
- Office : My Stars, My Uploads, My Outbox, My Excerpts, My Comments
- Tickets : Projects, Sites, Active tickets, Tickets, My known problems, Unassigned Tickets
- Clocking : Sessions
- Reports :
  - System : Broken GFKs
  - Clocking : Service Reports
- Configure :
  - System : Site Parameters, Help Texts, Users
  - Places : Countries, Places
  - Contacts : Organization types, Functions, List Types
  - Office : Upload Types, Excerpt Types, My Text Field Templates
  - Tickets : Project Types, Ticket types, Faculties (tree), Competences
  - Clocking : Session Types
- Explorer :
  - System : content types, Authorities, User Profiles, Notifications, Changes
  - Contacts : Contact Persons, List memberships
  - Office : Stars, Uploads, Upload Areas, Outgoing Mails, Attachments, Excerpts, Comments, Text Field Templates
  - Tickets : Milestones, Dependencies, Interests, Deployments
  - Faculties : Faculties (all), Competences
  - Clocking : Sessions
- Site : About