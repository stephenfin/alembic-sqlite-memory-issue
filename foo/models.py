# Copyright (c) 2011 X.commerce, a business unit of eBay Inc.
# Copyright 2010 United States Government as represented by the
# Administrator of the National Aeronautics and Space Administration.
# Copyright 2011 Piston Cloud Computing, Inc.
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.
"""
SQLAlchemy models for nova data.
"""

from oslo_config import cfg
from oslo_db.sqlalchemy import models
import sqlalchemy as sa
import sqlalchemy.dialects.mysql
from sqlalchemy.ext import declarative
from sqlalchemy import orm

CONF = cfg.CONF
BASE = declarative.declarative_base()


class NovaBase(models.TimestampMixin,
               models.ModelBase):
    metadata = None

    def __copy__(self):
        """Implement a safe copy.copy().

        SQLAlchemy-mapped objects travel with an object
        called an InstanceState, which is pegged to that object
        specifically and tracks everything about that object.  It's
        critical within all attribute operations, including gets
        and deferred loading.   This object definitely cannot be
        shared among two instances, and must be handled.

        The copy routine here makes use of session.merge() which
        already essentially implements a "copy" style of operation,
        which produces a new instance with a new InstanceState and copies
        all the data along mapped attributes without using any SQL.

        The mode we are using here has the caveat that the given object
        must be "clean", e.g. that it has no database-loaded state
        that has been updated and not flushed.   This is a good thing,
        as creating a copy of an object including non-flushed, pending
        database state is probably not a good idea; neither represents
        what the actual row looks like, and only one should be flushed.

        """
        session = orm.Session()

        copy = session.merge(self, load=False)
        session.expunge(copy)
        return copy


class VolumeUsage(BASE, NovaBase, models.SoftDeleteMixin):
    """Cache for volume usage data pulled from the hypervisor."""
    __tablename__ = 'volume_usage_cache'
    __table_args__ = ()
    id = sa.Column(sa.Integer, primary_key=True, nullable=False)
    volume_id = sa.Column(sa.String(36), nullable=False)
    instance_uuid = sa.Column(sa.String(36))
    project_id = sa.Column(sa.String(36))
    user_id = sa.Column(sa.String(64))
    availability_zone = sa.Column(sa.String(255))
    tot_last_refreshed = sa.Column(sa.DateTime)
    tot_reads = sa.Column(sa.BigInteger, default=0)
    tot_read_bytes = sa.Column(sa.BigInteger, default=0)
    tot_writes = sa.Column(sa.BigInteger, default=0)
    tot_write_bytes = sa.Column(sa.BigInteger, default=0)
    curr_last_refreshed = sa.Column(sa.DateTime)
    curr_reads = sa.Column(sa.BigInteger, default=0)
    curr_read_bytes = sa.Column(sa.BigInteger, default=0)
    curr_writes = sa.Column(sa.BigInteger, default=0)
    curr_write_bytes = sa.Column(sa.BigInteger, default=0)
