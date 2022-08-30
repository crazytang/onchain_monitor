from django.db import models

from onchain_monitor.models.base_model import BaseModel


class ContractMethodHash(BaseModel, models.Model):
    id = models.AutoField(primary_key=True)
    method_hash = models.CharField(max_length=100)
    method_hash_short = models.CharField(max_length=10)
    contract_name = models.CharField(max_length=500)
    method_sign = models.CharField(max_length=100)
    method_type = models.CharField(max_length=20)
    is_user = models.IntegerField()
    action_name = models.CharField(max_length=50)
    class_name = models.CharField(max_length=50)
    emitted_num = models.IntegerField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        db_table = 'tb_contract_method_hash'