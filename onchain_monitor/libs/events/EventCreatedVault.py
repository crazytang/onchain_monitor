from onchain_monitor.libs.events.EventBase import EventBase


class EventCreatedVault (EventBase):
    user_address: str
    collateral_token_address: str
    new_cai_amount: str
    amount: str
    
    def fetchTo(self, data: []):
        self.user_address = data[0]
        self.collateral_token_address = data[1]
        self.new_cai_amount = str(data[2])
        self.amount = str(data[3])