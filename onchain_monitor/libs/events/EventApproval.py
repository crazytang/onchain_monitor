from onchain_monitor.libs.events.EventBase import EventBase


class EventApproval(EventBase):
    owner: str
    spender: str
    amount: str

    def fetchTo(self, data: []):
        self.owner = data[0]
        self.spender = data[1]
        self.amount = str(data[2])