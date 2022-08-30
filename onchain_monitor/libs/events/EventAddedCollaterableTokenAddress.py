
from onchain_monitor.libs.events.EventBase import EventBase


class EventAddedCollaterableTokenAddress(EventBase):
    collateral_token_address = []

    def fetchTo(self, data: []) :
        self.collateral_token_address = data[0]