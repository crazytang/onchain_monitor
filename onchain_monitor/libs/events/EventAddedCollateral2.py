from onchain_monitor.libs.events.EventBase import EventBase


class EventAddedCollateral2(EventBase):
    user_address: str
    collateral_token_address: str
    amount: str
    new_cai_amount: str

    def fetchTo(self, data:[]):
        self.user_address = data[0]
        self.collateral_token_address = data[1]
        self.amount = str(data[2])
        self.new_cai_amount = str(data[3])