from unittest import TestCase

from oc_django.helpers.utils import get_param_data
from onchain_monitor.libs.events import EventAddedCollaterableTokenAddress, EventAddedCollateral, EventAddedCollateral2, EventApproval, EventClaimedCmk, EventCreatedVault, EventInit, EventIntegrityRestored, EventRepayedCAI, EventSetRestakePeriod, EventSettleInterestForBorrower, EventSetUnstakeCoolDownPeriod, EventStake, EventStakedCaiToken, EventTransfer, EventUnFreezing, EventUnStake, EventUnstakedCaiToken, EventUnStakedInFreezing, EventUpdatedCollaterableTokenAddresses, EventUserRestake, EventWithdrawCai, EventWithdrawedCAI, EventWithdrawedCaiInLiquidatePool, EventWithdrawedCmk, EventWithdrawedCollateral

class TestSwitch(TestCase):

    def setUp(self) -> None:
        pass

    def test_switch(self):

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

        method_sign = 'CreatedVault(address,address,uint256,uint256)'
        class_name = 'EventCreatedVault'
        data = '0000000000000000000000009b7094506d15dd2977b688a22bbb6df5501549e7000000000000000000000000f561f5a97a09edacb0f09765379c217b3496bb50000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000006f05b59d3b20000'

        param_data = get_param_data(method_sign, data)
        print('param_data', param_data)

        d = []
        for v in param_data:
            d.append(v['value'])
        rs = switch[class_name]()
        rs.fetchTo(d)
        print('rs', rs)