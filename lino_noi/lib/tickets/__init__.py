# Copyright 2008-2017 Luc Saffre
# License: BSD (see file COPYING for details)
"""
Adds functionality for managing tickets.

.. autosummary::
   :toctree:

    roles
    models
    ui
    choicelists


"""

from lino.api import ad, _


class Plugin(ad.Plugin):
    "See :class:`lino.core.plugin.Plugin`."

    verbose_name = _("Tickets")

    needs_plugins = [
        # 'lino_xl.lib.stars',
        'lino_xl.lib.excerpts',
        # 'lino_xl.lib.topics',
        'lino.modlib.comments',
        # 'lino.modlib.changes',
        'lino_noi.lib.noi']

    end_user_model = 'users.User'

    def on_site_startup(self, site):
        self.end_user_model = site.models.resolve(self.end_user_model)
        super(Plugin, self).on_site_startup(site)
        
    def setup_main_menu(self, site, profile, m):
        p = self.get_menu_group()
        m = m.add_menu(p.app_label, p.verbose_name)
        m.add_action('tickets.MyTickets')
        m.add_action('tickets.SuggestedTickets')
        # m.add_action('tickets.TicketsToDo')
        # m.add_action('tickets.MyOwnedTickets')
        m.add_action('tickets.ActiveTickets')
        m.add_action('tickets.AllTickets')
        # m.add_action('tickets.MyKnownProblems')
        m.add_action('tickets.UnassignedTickets')
        m.add_action('tickets.ActiveProjects')

    def setup_config_menu(self, site, profile, m):
        p = self.get_menu_group()
        m = m.add_menu(p.app_label, p.verbose_name)
        m.add_action('tickets.AllProjects')
        m.add_action('tickets.TopLevelProjects')
        m.add_action('tickets.ProjectTypes')
        m.add_action('tickets.TicketTypes')
        m.add_action('tickets.AllSites')

    def setup_explorer_menu(self, site, profile, m):
        p = self.get_menu_group()
        m = m.add_menu(p.app_label, p.verbose_name)
        # m.add_action('tickets.Projects')
        m.add_action('tickets.Links')
        m.add_action('tickets.TicketStates')
        
    def get_dashboard_items(self, user):
        if user.authenticated:
            yield self.site.actors.tickets.MyTickets
            yield self.site.actors.tickets.SuggestedTickets
        else:
            yield self.site.actors.tickets.PublicTickets
