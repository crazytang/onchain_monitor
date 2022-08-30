from onchain_monitor.libs.events.EventBase import EventBase


class EventSettleInterestForBorrower(EventBase):
    collateral_token_address: str
    collateral_interest_collected: str

    def fetchTo(self, data: []) :
        self.collateral_token_address = data[0]
        self.collateral_interest_collected = data[1]