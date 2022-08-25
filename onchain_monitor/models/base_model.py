from decimal import Decimal

from django.db.models.fields import DateTimeField
from django.db.models.fields.related import ManyToManyField


class BaseModel:
    def toJson(self):
        import json
        return json.dumps(self.toDict())

    def toDict(self, fields=None, exclude=None):
        data = {}
        for f in self._meta.concrete_fields + self._meta.many_to_many:
            value = f.value_from_object(self)

            if fields and f.name not in fields:
                continue

            if exclude and f.name in exclude:
                continue

            if isinstance(f, ManyToManyField):
                value = [i.id for i in value] if self.pk else None

            elif isinstance(f, DateTimeField):
                value = value.strftime('%Y-%m-%d %H:%M:%S') if value else None

            elif isinstance(value, Decimal):
                value = float(value)

            data[f.name] = value

        return data

    def __str__(self):
        return str(self.__dict__)

    def __repr__(self):
        return str(self.__dict__)
