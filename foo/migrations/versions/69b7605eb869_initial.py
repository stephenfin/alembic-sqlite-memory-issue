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

"""Initial version.

Revision ID: 69b7605eb869
Revises:
Create Date: 2021-07-07 16:49:54.196975
"""

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '69b7605eb869'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'foo',
        sa.Column('id', sa.Integer, primary_key=True, nullable=False),
        sa.Column('uuid', sa.String(36), nullable=True),
    )

    # change the 'uuid' column to non-nullable
    with op.batch_alter_table('foo') as batch_op:
        batch_op.alter_column('uuid', nullable=False)


def downgrade():
    pass
