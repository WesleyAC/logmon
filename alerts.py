from enum import Enum

class EventType(Enum):
    triggered = 1
    recovered = 2

class AlertEvent:
    def __init__(self, event_type, hits, time):
        self.event_type = event_type
        self.hits = hits
        self.time = time

    def __str__(self):
        if self.event_type == EventType.triggered:
            return "High traffic generated an alert - hits = {}, triggered at {}".format(self.hits, self.time)
        else:
            return "Alert recovered at {}".format(self.time)

class AlertManager:
    """
    The AlertManager keeps track of the little bit of state needed to keep
    track of alerts.

    Some other code should call `update` regularly, which will cause the
    AlertManager to log alerts and recoveries as they occur.
    """
    def __init__(self, alert_threshold):
        self.alerts = []
        self.in_alert = False
        self.alert_threshold = alert_threshold

    def update(self, hits, time):
        if hits >= self.alert_threshold and not self.in_alert:
            self.alerts.append(AlertEvent(EventType.triggered, hits, time))
            self.in_alert = True
        elif hits < self.alert_threshold and self.in_alert:
            self.alerts.append(AlertEvent(EventType.recovered, hits, time))
            self.in_alert = False

    def print_alerts(self, max_alerts):
        print("\n".join([str(e) for e in self.alerts[:max_alerts]]))
