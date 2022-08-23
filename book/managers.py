
from django.db import models

class QueryManager(models.Manager):

    def get_query_set(self):
        return super(QueryManager, self).get_query_set().filter(etat=0)
