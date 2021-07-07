# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

import os

from alembic import command as alembic_api
from alembic import config as alembic_config
from oslo_db.sqlalchemy import enginefacade
from oslo_log import log as logging

LOG = logging.getLogger(__name__)

context_manager = enginefacade.transaction_context()


def get_engine():
    return enginefacade.transaction_context()


def find_alembic_conf():
    """Get the path for the alembic repository."""
    path = os.path.join(
        os.path.abspath(os.path.dirname(__file__)), os.pardir, 'alembic.ini')

    config = alembic_config.Config(path)
    # we don't want to use the logger configuration from the file, which is
    # only really intended for the CLI
    # https://stackoverflow.com/a/42691781/613428
    config.attributes['configure_logger'] = False

    return config


def db_sync():
    """Migrate the database to `version` or the most recent version."""
    engine = get_engine()

    config = find_alembic_conf()
    # discard the URL encoded in alembic.ini in favour of the URL configured
    # for the engine by the database fixtures, casting from
    # 'sqlalchemy.engine.url.URL' to str in the process
    config.set_main_option('sqlalchemy.url', str(engine.url))

    LOG.info('Applying migration(s)')

    # re-use the connection rather than creating a new one
    with engine.begin() as connection:
        config.attributes['connection'] = connection
        alembic_api.upgrade(config, 'head')

    LOG.info('Migration(s) applied')
