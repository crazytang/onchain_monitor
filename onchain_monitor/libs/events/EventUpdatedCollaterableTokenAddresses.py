from onchain_monitor.libs.events.EventBase import EventBase


class EventUpdatedCollaterableTokenAddresses(EventBase):
    owner: str
    collateral_token_address: str

    def fetchTo(self, data: []) :
        self.owner = data[0]
        self.collateral_token_address = data[1]
  

