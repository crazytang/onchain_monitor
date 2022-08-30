from django.db.models import QuerySet

from onchain_monitor.models.contract_method_hash import ContractMethodHash


class ContractMethodHashService:
    @staticmethod
    def get_all() -> QuerySet:
        return ContractMethodHash.objects.all()

    @staticmethod
    def get_one_from_hash(method_hash:str) -> ContractMethodHash:
        return ContractMethodHash.objects.filter(method_hash=method_hash).first()