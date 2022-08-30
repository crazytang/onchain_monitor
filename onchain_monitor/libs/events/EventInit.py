from onchain_monitor.libs.events.EventBase import EventBase


class EventInit(EventBase):
    caller: str
    cai_maker_oracle_address: str

    def fetchTo(self, data: []):
        self.caller = data[0]
        self.cai_maker_oracle_address = data[1]
