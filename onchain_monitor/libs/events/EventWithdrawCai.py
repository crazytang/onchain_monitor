from onchain_monitor.libs.events.EventBase import EventBase


class EventWithdrawCai(EventBase):
    recipient_address: str
    amount: str

    def fetchTo(self, data: []) :
        self.recipient_address = data[0]
        self.amount = str(data[1])
  

