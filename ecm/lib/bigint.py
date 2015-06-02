from __future__ import absolute_import

from django.db import models
from django.utils.translation import ugettext_lazy as _

# Because Django is retarded and can't do auto incrementing 64bit ints by itself.
# Credit to Sentry for the implementation


class BigAutoField(models.AutoField):
        description = _("Big Integer")

        MAX_VALUE = 9223372036854775807

        def db_type(self, connection):
            engine = connection.settings_dict['ENGINE']
            if 'mysql' in engine:
                return "bigint AUTO_INCREMENT"
            elif 'oracle' in engine:
                return "NUMBER(19)"
            elif 'postgres' in engine:
                return "bigserial"
            # SQLite doesnt actually support bigints with auto incrementing
            elif 'sqlite' in engine:
                return 'integer'
            else:
                raise NotImplemented

        def get_related_db_type(self, connection):
            return models.BigIntegerField().db_type(connection)

        def get_internal_type(self):
            return "BigIntegerField"

        def get_prep_value(self, value):
            if value:
                value = long(value)
                assert value <= self.MAX_VALUE
            return super(BigAutoField, self).get_prep_value(value)