from faas_framework.aws.models.event_bridge import EventBridgeModel


def test_event_bridge_model(event_bridge_event_dict):
    EventBridgeModel(**event_bridge_event_dict)
