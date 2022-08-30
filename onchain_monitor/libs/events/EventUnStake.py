from onchain_monitor.libs.events.EventBase import EventBase


class EventUnStake(EventBase):
    user_address: str
    amount: str

    def fetchTo(self, data: []) :
        self.user_address = data[0]
        self.amount = str(data[1])
