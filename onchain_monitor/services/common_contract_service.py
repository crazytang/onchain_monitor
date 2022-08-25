from onchain_monitor.models.common_contract import CommonContract


class CommonContractService:
    @staticmethod
    def get_all(include_deleted=False):
        if include_deleted:
            return CommonContract.objects.all()

        return CommonContract.objects.all().filter(is_deleted=0)
