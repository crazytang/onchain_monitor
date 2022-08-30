from onchain_monitor.libs.events.EventBase import EventBase


class EventIntegrityRestored(EventBase):
    type: str
    method: str
    error_value: str

    def fetchTo(self, data: []) :
        self.type = data[0]
        self.method = data[1]
        self.error_value = str(data[2])
  

