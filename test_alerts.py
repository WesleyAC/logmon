import pytest

from datetime import datetime

from alerts import AlertManager, EventType

class TestAlerts:
    def test_no_alerts(self):
        a = AlertManager(100)
        for _ in range(25):
            a.update(25, datetime.now())
        assert len(a.alerts) == 0

    def test_alert_without_recovery(self):
        a = AlertManager(100)
        a.update(25, datetime.now())
        a.update(150, datetime.now())
        assert len(a.alerts) == 1
        assert a.alerts[0].event_type == EventType.triggered

    def test_alert_with_recovery(self):
        a = AlertManager(100)
        a.update(25, datetime.now())
        a.update(150, datetime.now())
        a.update(25, datetime.now())
        assert len(a.alerts) == 2
        assert a.alerts[0].event_type == EventType.triggered
        assert a.alerts[1].event_type == EventType.recovered

    def test_multiple_alerts(self):
        a = AlertManager(100)
        a.update(25, datetime.now())
        for _ in range(25):
            a.update(150, datetime.now())
            a.update(25, datetime.now())
        assert len(a.alerts) == 25*2
        assert len(list(filter(lambda x: x.event_type == EventType.triggered, a.alerts))) == 25
        assert len(list(filter(lambda x: x.event_type == EventType.recovered, a.alerts))) == 25

    def test_continious_alert(self):
        a = AlertManager(100)
        a.update(25, datetime.now())
        for _ in range(25):
            a.update(150, datetime.now())
        assert len(a.alerts) == 1
        assert a.alerts[0].event_type == EventType.triggered
