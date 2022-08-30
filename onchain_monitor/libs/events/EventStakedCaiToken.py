from onchain_monitor.libs.events.EventBase import EventBase


class EventStakedCaiToken(EventBase):
    sender: str
    amount: str

    def fetchTo(self, data: []) :
        self.sender = data[0]
        self.amount = str(data[1])
