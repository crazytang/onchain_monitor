from django.db import models

from onchain_monitor.models.base_model import BaseModel


class ContractTransactionInfo(BaseModel, models.Model):
    id = models.AutoField(primary_key=True)
    tx_hash = models.CharField(max_length=100)
    tx_status = models.IntegerField()
    tx_from = models.CharField(max_length=100)
    tx_to = models.CharField(max_length=100)
    tx_value = models.FloatField()
    block_hash = models.CharField(max_length=100)
    block_number = models.IntegerField()
    network = models.CharField(max_length=20)
    tx_nonce = models.IntegerField()
    tx_data = models.TextField()
    tx_receipt = models.TextField()
    tx_gas_used = models.FloatField()
    eth_price = models.FloatField()
    tx_fee = models.FloatField()
    transacted_at = models.DateTimeField()
    created_at = models.DateTimeField()

    class Meta:
        db_table = 'tb_contract_transaction_info'
