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

"""Initial version

Revision ID: 8f2f1571d55b
Revises:
Create Date: 2021-04-13 11:59:19.234123
"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy import types as sqla_types

# revision identifiers, used by Alembic.
revision = '8f2f1571d55b'
down_revision = None
branch_labels = None
depends_on = None


def _create_shadow_tables(migrate_engine):
    meta = sa.MetaData(migrate_engine)
    meta.reflect(migrate_engine)
    table_names = list(meta.tables.keys())

    meta.bind = migrate_engine

    for table_name in table_names:
        table = sa.Table(table_name, meta, autoload=True)

        columns = []
        for column in table.columns:
            column_copy = None
            # NOTE(boris-42): BigInteger is not supported by sqlite, so
            #                 after copy it will have NullType, other
            #                 types that are used in Nova are supported by
            #                 sqlite.
            if isinstance(column.type, sqla_types.NullType):
                column_copy = sa.Column(
                    column.name, sa.BigInteger(), default=0,
                )

            if column_copy is None:
                column_copy = column.copy()

            columns.append(column_copy)

        op.create_table(
            'shadow_' + table_name, meta, *columns, mysql_engine='InnoDB',
        )


def upgrade():
    bind = op.get_bind()

    op.create_table(
        'volume_usage_cache',
        sa.Column('created_at', sa.DateTime(timezone=False)),
        sa.Column('updated_at', sa.DateTime(timezone=False)),
        sa.Column('deleted_at', sa.DateTime(timezone=False)),
        sa.Column('id', sa.Integer(), primary_key=True, nullable=False),
        sa.Column('volume_id', sa.String(36), nullable=False),
        sa.Column('tot_last_refreshed', sa.DateTime(timezone=False)),
        sa.Column('tot_reads', sa.BigInteger(), default=0),
        sa.Column('tot_read_bytes', sa.BigInteger(), default=0),
        sa.Column('tot_writes', sa.BigInteger(), default=0),
        sa.Column('tot_write_bytes', sa.BigInteger(), default=0),
        sa.Column('curr_last_refreshed', sa.DateTime(timezone=False)),
        sa.Column('curr_reads', sa.BigInteger(), default=0),
        sa.Column('curr_read_bytes', sa.BigInteger(), default=0),
        sa.Column('curr_writes', sa.BigInteger(), default=0),
        sa.Column('curr_write_bytes', sa.BigInteger(), default=0),
        sa.Column('deleted', sa.Integer),
        sa.Column('instance_uuid', sa.String(length=36)),
        sa.Column('project_id', sa.String(length=36)),
        sa.Column('user_id', sa.String(length=36)),
        sa.Column('availability_zone', sa.String(length=255)),
        mysql_engine='InnoDB',
        mysql_charset='utf8'
    )

    _create_shadow_tables(bind.engine)

    # TODO(stephenfin): Fix these various bugs in a follow-up

    # 244_increase_user_id_length_volume_usage_cache; this alteration should
    # apply to shadow tables also

    with op.batch_alter_table('volume_usage_cache') as batch_op:
        batch_op.alter_column('user_id', type_=sa.String(64))


def downgrade():
    pass
