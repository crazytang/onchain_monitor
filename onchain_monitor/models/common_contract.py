from django.db import models

from onchain_monitor.models.base_model import BaseModel


class CommonContract(BaseModel, models.Model):
    id = models.AutoField(primary_key=True)
    contract_name = models.CharField(max_length=255)
    contract_symbol = models.CharField(max_length=10)
    contract_address = models.CharField(max_length=50)
    decimals = models.IntegerField()
    is_token = models.IntegerField()
    version = models.CharField(max_length=50)
    abi = models.TextField()
    network = models.CharField(max_length=50)
    remark = models.CharField(max_length=250)
    address_updated_at = models.DateTimeField()
    address_history = models.TextField()
    is_deleted = models.IntegerField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        db_table = 'tb_common_contract'