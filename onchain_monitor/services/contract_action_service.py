from __future__ import annotations

import datetime
import json

import eth_abi
import eth_utils
from web3.datastructures import AttributeDict

from oc_django.etherem.objects.contract_receipt import ContractReceipt
from oc_django.helpers.utils import get_prix_hash, get_param_data, get_datetime_now
from onchain_monitor.libs.enums.method_type import MethodType
from onchain_monitor.libs.events import EventAddedCollaterableTokenAddress, EventAddedCollateral, EventAddedCollateral2, EventApproval, EventClaimedCmk, EventCreatedVault, EventInit, EventIntegrityRestored, EventRepayedCAI, EventSetRestakePeriod, EventSettleInterestForBorrower, EventSetUnstakeCoolDownPeriod, EventStake, EventStakedCaiToken, EventTransfer, EventUnFreezing, EventUnStake, EventUnstakedCaiToken, EventUnStakedInFreezing, EventUpdatedCollaterableTokenAddresses, EventUserRestake, EventWithdrawCai, EventWithdrawedCAI, EventWithdrawedCaiInLiquidatePool, EventWithdrawedCmk, EventWithdrawedCollateral
from onchain_monitor.models.contract_action import ContractAction
from onchain_monitor.models.contract_method_hash import ContractMethodHash
from onchain_monitor.models.contract_transaction_info import ContractTransactionInfo
from onchain_monitor.services.contract_method_hash_service import ContractMethodHashService


class ContractActionService:
    @staticmethod
    def get_one(method_hash:str, contract_address:str, from_address:str, log_index:int, operated_at) -> ContractAction:
        return ContractAction.objects.filter(method_hash=method_hash, contract_address=contract_address, from_address=from_address, log_index=log_index, operated_at=operated_at).first()

    @staticmethod
    def save_function_data(tx_info: ContractTransactionInfo, method_hashes: [ContractMethodHash]) -> ContractMethodHash|None:
        """
        saving function data to DB
        """
        method_hash_info: ContractMethodHash|None = None
        for m in method_hashes:
            if get_prix_hash(tx_info.tx_data).lower() == m.method_hash_short.lower():
                method_hash_info = m

        if not method_hash_info or type(method_hash_info) != ContractMethodHash:
            return

        print('matched function hash', method_hash_info.method_hash_short, method_hash_info.method_sign)
        contract_action = ContractActionService.get_one(method_hash=method_hash_info.method_hash, contract_address=tx_info.tx_to, from_address=tx_info.tx_from, log_index=0, operated_at=tx_info.transacted_at)
        if not contract_action:
            contract_action = ContractAction()
            contract_action.method_hash = method_hash_info.method_hash

        contract_action.tx_hash = tx_info.tx_hash
        contract_action.contract_address = tx_info.tx_to
        contract_action.from_address = tx_info.tx_from
        contract_action.network = tx_info.network
        contract_action.method_hash_short = method_hash_info.method_hash_short
        contract_action.method_sign = method_hash_info.method_sign
        contract_action.method_type = MethodType.function.value
        contract_action.action_name = method_hash_info.action_name
        contract_action.action_params = json.dumps(get_param_data(method_hash_info.method_sign, tx_info.tx_data))
        contract_action.operated_data = None
        contract_action.log_index = 0
        contract_action.is_user = method_hash_info.is_user
        contract_action.operated_at = tx_info.transacted_at
        contract_action.created_at = get_datetime_now()

        contract_action.save()

        ContractActionService.save_events_data(tx_info, method_hashes)

    @staticmethod
    def save_events_data(tx_info: ContractTransactionInfo, method_hashes: [ContractMethodHash]):
        """
        saving events data to DB
        """
        tx_receipt = json.loads(tx_info.tx_receipt)
        logs = tx_receipt['logs']

        for log in logs:
            topics = log['topics']
            method_hash = topics[0]

            method_hash_info: ContractMethodHash|None = None
            for m in method_hashes:
                if method_hash.lower() == m.method_hash.lower():
                    method_hash_info = m
                    break

            if not method_hash_info:
                continue

            print('matched event method_hash', method_hash_info.method_hash, method_hash_info.method_sign, log['logIndex'])
            data = ''
            for i in range(1, len(topics)):
                data += topics[i][2:]

            data += log['data'][2:]

            method_sign = method_hash_info.method_sign
            param_data = get_param_data(method_sign, data)
            operated_data = ContractActionService._fetch_to_operated_data(method_hash_info.class_name, param_data)

            contract_action = ContractActionService.get_one(method_hash=method_hash_info.method_hash, contract_address=tx_info.tx_to, from_address=tx_info.tx_from, log_index=log['logIndex'], operated_at=tx_info.transacted_at)
            if not contract_action:
                contract_action = ContractAction()
                contract_action.method_hash = method_hash_info.method_hash

            contract_action.tx_hash = tx_info.tx_hash
            contract_action.contract_address = tx_info.tx_to
            contract_action.from_address = tx_info.tx_from
            contract_action.network = tx_info.network
            contract_action.method_hash_short = method_hash_info.method_hash_short
            contract_action.method_sign = method_hash_info.method_sign
            contract_action.method_type = MethodType.event.value
            contract_action.action_name = method_hash_info.action_name
            print('param_data', param_data)
            print('operated_data', operated_data, type(operated_data))
            contract_action.action_params = json.dumps(param_data)
            contract_action.operated_data = operated_data.toJson() if operated_data else None
            contract_action.log_index = log['logIndex']
            contract_action.is_user = method_hash_info.is_user
            contract_action.operated_at = tx_info.transacted_at
            contract_action.created_at = get_datetime_now()

            contract_action.save()


    @staticmethod
    def _fetch_to_operated_data( class_name, param_data):
        if class_name == '':
            return

        switch ={
            'EventAddedCollaterableTokenAddress': EventAddedCollaterableTokenAddress.EventAddedCollaterableTokenAddress,
            'EventAddedCollateral': EventAddedCollateral.EventAddedCollateral,
            'EventAddedCollateral2': EventAddedCollateral2.EventAddedCollateral2,
            'EventApproval': EventApproval.EventApproval,
            'EventClaimedCmk': EventClaimedCmk.EventClaimedCmk,
            'EventCreatedVault': EventCreatedVault.EventCreatedVault,
            'EventInit': EventInit.EventInit,
            'EventIntegrityRestored': EventIntegrityRestored.EventIntegrityRestored,
            'EventRepayedCAI': EventRepayedCAI.EventRepayedCAI,
            'EventSetRestakePeriod': EventSetRestakePeriod.EventSetRestakePeriod,
            'EventSettleInterestForBorrower': EventSettleInterestForBorrower.EventSettleInterestForBorrower,
            'EventSetUnstakeCoolDownPeriod': EventSetUnstakeCoolDownPeriod.EventSetUnstakeCoolDownPeriod,
            'EventStake': EventStake.EventStake,
            'EventStakedCaiToken': EventStakedCaiToken.EventStakedCaiToken,
            'EventTransfer': EventTransfer.EventTransfer,
            'EventUnFreezing': EventUnFreezing.EventUnFreezing,
            'EventUnStake': EventUnStake.EventUnStake,
            'EventUnstakedCaiToken': EventUnstakedCaiToken.EventUnstakedCaiToken,
            'EventUnStakedInFreezing': EventUnStakedInFreezing.EventUnStakedInFreezing,
            'EventUpdatedCollaterableTokenAddresses': EventUpdatedCollaterableTokenAddresses.EventUpdatedCollaterableTokenAddresses,
            'EventUserRestake': EventUserRestake.EventUserRestake,
            'EventWithdrawCai': EventWithdrawCai.EventWithdrawCai,
            'EventWithdrawedCAI': EventWithdrawedCAI.EventWithdrawedCAI,
            'EventWithdrawedCaiInLiquidatePool': EventWithdrawedCaiInLiquidatePool.EventWithdrawedCaiInLiquidatePool,
            'EventWithdrawedCmk': EventWithdrawedCmk.EventWithdrawedCmk,
            'EventWithdrawedCollateral': EventWithdrawedCollateral.EventWithdrawedCollateral,
        }
        if not param_data or class_name not in switch:
            return {}
        data = []
        print('matched event class', class_name )
        for param in param_data:
            data.append(param['value'])

        obj = switch[class_name]()
        obj.fetchTo(data)

        return obj