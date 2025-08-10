from django.db import models


class CoreQuerySet(models.query.QuerySet):

    def with_id(self, id):
        return self.filter(id=id)

    def with_id_in(self, ids):
        return self.filter(id__in=ids)
