from oc_django.etherem.ethereum_service import EthereumService
from onchain_monitor.services.contract_action_service import ContractActionService
from onchain_monitor.services.contract_method_hash_service import ContractMethodHashService
from onchain_monitor.services.contract_transaction_service import ContractTransactionService


class TxDataService:
    @staticmethod
    def handle(data):
        tx_hash = data['tx_hash']
        network = data['network']
        ethereum_service = EthereumService(network)
        tx = ethereum_service.get_contract_transaction(tx_hash)
        if tx.hash == '':
            print('%s tx_hash is not exists in %s' %(tx_hash, network))
            return
        receipt, raw_receipt = ethereum_service.wait_raw_transaction_receipt(tx_hash)

        block = ethereum_service.get_block_from_number(receipt.blockNumber)

        tx_info = ContractTransactionService.handleTx(block, tx, receipt, raw_receipt, network)
        all_methods = ContractMethodHashService.get_all()

        ContractActionService.save_function_data(tx_info, all_methods)


