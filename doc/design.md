# class diagram
```mermaid
classDiagram
class BaseDevice {
+simulate_actions(action, duration)
-rate
}
class UHID {
+dispatch()
-_process_one_event()
set_report(req, rnum, rtype, data)
+call_input_event()
}
class Endpoint
class Brain {
<<abstract>>
+set_report(req, rnum, rtype, data)
}
class PhysHWComponent {
<<Interface>>
+setNewState(**kwargs)
+getState()
}
class LED {
+brigthness
}
class RGBLed {
+red
+green
+blue
}
class HIDActuator {
+name
+value
+report_id
+get_HID_data(data, action)
}
class OpticalSensor {
+dpi
}
class Button
class Wheel
class LogitechHIDPP20Brain
class SteelSeriesBrain
BaseDevice o-- Endpoint : <dict> endpoints
BaseDevice o-- Brain : brain
BaseDevice o-- PhysHWComponent : <dict> physical_parts
BaseDevice o-- HIDActuator: <dict> HID_parts
UHID <|-- Endpoint
PhysHWComponent <|-- LED
PhysHWComponent <|-- RGBLed
Brain <|-- LogitechHIDPP20Brain
Brain <|-- SteelSeriesBrain
HIDActuator<|--OpticalSensor
HIDActuator<|--Button
HIDActuator<|--Wheel
```

---

# Sequence diagram for `dispatch()`:
```mermaid
sequenceDiagram
participant CI client
participant BaseDevice
participant UHID
CI client->> @UHID: dispatch()
@UHID-->> Endpoint: _process_one_event()
Endpoint->>BaseDevice: set_report(req, rnum, rtype, data)
BaseDevice->>Brain: set_report(req, rnum, rtype, data)
Brain->>BaseDevice: set_new_state("RGB1", red: 255)
BaseDevice->>RGBLed: set_new_state(red: 255)
```

---

# Sequence diagram for `simulate_actions()` (refresh rate: 1Hz):
```mermaid
sequenceDiagram
CI client->>BaseDevice: simulate_actions(move: {x:3}, duration: 3s)
BaseDevice->>BaseDevice : individual_action = {move: {x: 1}}
BaseDevice->>BaseDevice : data = {}
BaseDevice->>HIDActuator: for each: get_HID_data(data, individual_action)
HIDHWComponent->>HIDActuator: <OpticalSensor> `if move in action and self.name in action[move]:  data[self.report_id]`[self.name] = 1
BaseDevice->>Endpoint : for each: call_input_event(data[endpoint.report_id])
BaseDevice->>Endpoint : for each: call_input_event(data[endpoint.report_id])
BaseDevice->>Endpoint : for each: call_input_event(data[endpoint.report_id])
```

# Notes

- `Brain` can not inherit from `UHID` or `EndPoint`: it needs to process all endpoints in one place
- `rate` is global to `SimulatedDevice` because it's a parameter only used in `simulate_actions()`, and it doesn't really make sense to have a special class for it

