from django.db import models

from onchain_monitor.libs.enums.method_type import MethodType
from onchain_monitor.models.base_model import BaseModel


class ContractAction(BaseModel, models.Model):
    id = models.AutoField(primary_key=True)
    contract_address = models.CharField(max_length=50)
    from_address = models.CharField(max_length=50)
    tx_hash = models.CharField(max_length=100)
    network = models.CharField(max_length=20)
    method_hash = models.CharField(max_length=100)
    method_hash_short = models.CharField(max_length=10)
    method_sign = models.CharField(max_length=100)
    method_type = models.CharField(max_length=20)
    action_name = models.CharField(max_length=50)
    action_params = models.CharField(max_length=2000)
    operated_data = models.CharField(max_length=2000)
    log_index = models.IntegerField()
    is_user = models.IntegerField()
    operated_at = models.DateTimeField()
    created_at = models.DateTimeField()

    class Meta:
        db_table = 'tb_contract_action'
