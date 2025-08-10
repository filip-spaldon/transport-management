from django.db import models


class ModelWithTimestamps(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class CoreModel(ModelWithTimestamps):
    class Meta:
        abstract = True

    def get_standard_str_representation(self):
        representation = f"#{self.id} {self.__class__.__name__}"
        if hasattr(self, "name"):
            representation += f" - {self.name}"
        return representation

    def __str__(self):
        return self.get_standard_str_representation()
