#
# This file is part of pretix (Community Edition).
#
# Copyright (C) 2014-2020 Raphael Michel and contributors
# Copyright (C) 2020-2021 rami.io GmbH and contributors
#
# This program is free software: you can redistribute it and/or modify it under the terms of the GNU Affero General
# Public License as published by the Free Software Foundation in version 3 of the License.
#
# ADDITIONAL TERMS APPLY: Pursuant to Section 7 of the GNU Affero General Public License, additional terms are
# applicable granting you additional permissions and placing additional restrictions on your usage of this software.
# Please refer to the pretix LICENSE file to obtain the full terms applicable to this work. If you did not receive
# this file, see <https://pretix.eu/about/en/license>.
#
# This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied
# warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Affero General Public License for more
# details.
#
# You should have received a copy of the GNU Affero General Public License along with this program.  If not, see
# <https://www.gnu.org/licenses/>.
#
import hashlib

from django.conf import settings
from django.core.cache import cache
from django.core.files.base import ContentFile, File
from django.core.files.storage import default_storage
from django.core.management.base import BaseCommand
from django_scopes import scopes_disabled

from pretix.base.settings import GlobalSettingsObject
from pretix.presale.views.widget import generate_widget_js


class Command(BaseCommand):
    help = "Re-generate runtime-generated assets and scripts"

    def add_arguments(self, parser):
        parser.add_argument('--organizer', action='store', type=str)
        parser.add_argument('--event', action='store', type=str)

    @scopes_disabled()
    def handle(self, *args, **options):
        gs = GlobalSettingsObject()
        for lc, ll in settings.LANGUAGES:
            data = generate_widget_js(lc).encode()
            checksum = hashlib.sha1(data).hexdigest()
            fname = gs.settings.get('widget_file_{}'.format(lc))
            if not fname or gs.settings.get('widget_checksum_{}'.format(lc), '') != checksum:
                newname = default_storage.save(
                    'pub/widget/widget.{}.{}.js'.format(lc, checksum),
                    ContentFile(data)
                )
                gs.settings.set('widget_file_{}'.format(lc), 'file://' + newname)
                gs.settings.set('widget_checksum_{}'.format(lc), checksum)
                cache.delete('widget_js_data_{}'.format(lc))
                if fname:
                    if isinstance(fname, File):
                        default_storage.delete(fname.name)
                    else:
                        default_storage.delete(fname)
