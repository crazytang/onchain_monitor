from onchain_monitor.libs.events.EventBase import EventBase


class EventRepayedCAI(EventBase):
    user_address: str
    collateral_token_address: str
    amount: str
    
    def fetchTo(self, data: []):
        self.user_address = data[0]
        self.collateral_token_address = data[1]
        self.amount = str(data[2])
