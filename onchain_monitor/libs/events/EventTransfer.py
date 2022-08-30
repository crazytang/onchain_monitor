from onchain_monitor.libs.events.EventBase import EventBase


class EventTransfer(EventBase):
    _from: str
    to: str
    value: str

    def fetchTo(self, data: []) :
        self._from = data[0]
        self.to = data[1]
        self.value = str(data[2])
