from django.db import models

from .base_model import BaseModel


class Contract(BaseModel, models.Model):
    id = models.AutoField(primary_key=True)
    project_id = models.IntegerField()
    contract_name = models.CharField(max_length=255)
    contract_address = models.CharField(max_length=50)
    network = models.CharField(max_length=50)
    network_id = models.IntegerField()
    chain_id = models.IntegerField()
    remark = models.CharField(max_length=250)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    deleted_at = models.DateTimeField()

    class Meta:
        db_table = 'oc_contract'