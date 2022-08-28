from onchain_monitor.models.common_contract import CommonContract


class CommonContractService:
    @staticmethod
    def get_all(include_deleted=False):
        if include_deleted:
            return CommonContract.objects.all()

        return CommonContract.objects.all().filter(is_deleted=0)

    @staticmethod
    def get_contract_addresses() -> [str]:
        rs = CommonContractService.get_all()

        addresses: [str] = []
        for i in range(0, len(rs)):
            addresses.append(rs[i].contract_address.lower())

        return addresses