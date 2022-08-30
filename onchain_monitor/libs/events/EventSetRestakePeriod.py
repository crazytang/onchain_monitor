from onchain_monitor.libs.events.EventBase import EventBase


class EventSetRestakePeriod(EventBase):
    owner: str
    period_in_seconds: int

    def fetchTo(self, data: []):
        self.owner = data[0]
        self.period_in_seconds = int(data[1])
