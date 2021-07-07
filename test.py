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

from unittest import mock

from oslo_db.sqlalchemy import enginefacade
from oslo_db.sqlalchemy import test_fixtures
from oslo_db.sqlalchemy import test_migrations
import testtools

from foo import migration
from foo import models


class ModelsMigrationsSync(test_migrations.ModelsMigrationsSync):

    def setUp(self):
        super().setUp()
        self.engine = enginefacade.writer.get_engine()

    def db_sync(self, engine):
        with mock.patch.object(migration, 'get_engine', return_value=engine):
            migration.db_sync()

    def get_engine(self):
        return self.engine

    def get_metadata(self):
        return models.BASE.metadata


class TestModelsSyncSQLite(
    ModelsMigrationsSync,
    test_fixtures.OpportunisticDBTestMixin,
    testtools.TestCase,
):
    pass
