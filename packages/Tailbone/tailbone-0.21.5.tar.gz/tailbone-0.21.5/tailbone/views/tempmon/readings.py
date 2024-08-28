# -*- coding: utf-8; -*-
################################################################################
#
#  Rattail -- Retail Software Framework
#  Copyright © 2010-2023 Lance Edgar
#
#  This file is part of Rattail.
#
#  Rattail is free software: you can redistribute it and/or modify it under the
#  terms of the GNU General Public License as published by the Free Software
#  Foundation, either version 3 of the License, or (at your option) any later
#  version.
#
#  Rattail is distributed in the hope that it will be useful, but WITHOUT ANY
#  WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
#  FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more
#  details.
#
#  You should have received a copy of the GNU General Public License along with
#  Rattail.  If not, see <http://www.gnu.org/licenses/>.
#
################################################################################
"""
Views for tempmon readings
"""

from sqlalchemy import orm

from rattail_tempmon.db import model as tempmon

from webhelpers2.html import tags

from tailbone.views.tempmon import MasterView


class TempmonReadingView(MasterView):
    """
    Master view for tempmon readings.
    """
    model_class = tempmon.Reading
    model_title = "TempMon Reading"
    model_title_plural = "TempMon Readings"
    route_prefix = 'tempmon.readings'
    url_prefix = '/tempmon/readings'
    creatable = False
    editable = False
    bulk_deletable = True

    grid_columns = [
        'client_key',
        'client_host',
        'probe',
        'taken',
        'degrees_f',
    ]

    form_fields = [
        'client',
        'probe',
        'taken',
        'degrees_f',
    ]

    def query(self, session):
        return session.query(tempmon.Reading)\
                      .join(tempmon.Client)\
                      .options(orm.joinedload(tempmon.Reading.client))

    def configure_grid(self, g):
        super().configure_grid(g)

        # client_key
        g.set_sorter('client_key', tempmon.Client.config_key)
        g.set_filter('client_key', tempmon.Client.config_key)

        # client_host
        g.set_sorter('client_host', tempmon.Client.hostname)
        g.set_filter('client_host', tempmon.Client.hostname)

        # probe
        g.set_joiner('probe', lambda q: q.join(tempmon.Probe,
                                               tempmon.Probe.uuid == tempmon.Reading.probe_uuid))
        g.set_sorter('probe', tempmon.Probe.description)
        g.set_filter('probe', tempmon.Probe.description)

        g.set_sort_defaults('taken', 'desc')
        g.set_type('taken', 'datetime')

        g.set_renderer('client_key', self.render_client_key)
        g.set_renderer('client_host', self.render_client_host)

        g.set_link('probe')
        g.set_link('taken')

    def render_client_key(self, reading, column):
        return reading.client.config_key

    def render_client_host(self, reading, column):
        return reading.client.hostname

    def configure_form(self, f):
        super().configure_form(f)

        # client
        f.set_renderer('client', self.render_client)
        f.set_label('client', "Tempmon Client")

        # probe
        f.set_renderer('probe', self.render_probe)
        f.set_label('probe', "Tempmon Probe")

    def render_client(self, reading, field):
        client = reading.client
        if not client:
            return ""
        text = str(client)
        url = self.request.route_url('tempmon.clients.view', uuid=client.uuid)
        return tags.link_to(text, url)

    def render_probe(self, reading, field):
        probe = reading.probe
        if not probe:
            return ""
        text = str(probe)
        url = self.request.route_url('tempmon.probes.view', uuid=probe.uuid)
        return tags.link_to(text, url)


def defaults(config, **kwargs):
    base = globals()

    TempmonReadingView = kwargs.get('TempmonReadingView', base['TempmonReadingView'])
    TempmonReadingView.defaults(config)


def includeme(config):
    defaults(config)
