from enum import Enum


class Steps(str, Enum):
    DEVICE_DETECTED = "DEVICE_DETECTED"
    AUTH_STARTED = "AUTH_STARTED"
    AUTH_SUCCESS = "AUTH_SUCCESS"
    RANGING_STARTED = "RANGING_STARTED"
    PROXIMITY_VALIDATED = "PROXIMITY_VALIDATED"
    UNLOCK_REQUESTED = "UNLOCK_REQUESTED"
    UNLOCK_CONFIRMED = "UNLOCK_CONFIRMED"
    SESSION_TERMINATED = "SESSION_TERMINATED"


STEP_MAPPING = {
    "Digital Key device detected": Steps.DEVICE_DETECTED,
    "Session initiated": Steps.AUTH_STARTED,
    "Authentication successful": Steps.AUTH_SUCCESS,
    "Ranging session started": Steps.RANGING_STARTED,
    "Proximity validated": Steps.PROXIMITY_VALIDATED,
    "Door unlock command issued": Steps.UNLOCK_REQUESTED,
    "Door unlock confirmed": Steps.UNLOCK_CONFIRMED,
    "Session terminated": Steps.SESSION_TERMINATED
}


class STATE(str, Enum):
    IDLE = "IDLE"
    DETECTED = "DETECTED"
    AUTHENTICATING = "AUTHENTICATING"
    AUTHENTICATED = "AUTHENTICATED"
    RANGING = "RANGING"
    PROXIMITY_CONFIRMED = "PROXIMITY_CONFIRMED"
    ACCESS_REQUESTED = "ACCESS_REQUESTED"
    ACCESS_GRANTED = "ACCESS_GRANTED"
    TERMINATED = "TERMINATED"


STATE_TRANSITION_MAP = {
    STATE.IDLE: [STATE.DETECTED],
    STATE.DETECTED: [STATE.AUTHENTICATING],
    STATE.AUTHENTICATING: [STATE.AUTHENTICATED],
    STATE.AUTHENTICATED: [STATE.RANGING],
    STATE.RANGING: [STATE.PROXIMITY_CONFIRMED],
    STATE.PROXIMITY_CONFIRMED: [STATE.ACCESS_REQUESTED],
    STATE.ACCESS_REQUESTED: [STATE.ACCESS_GRANTED],
    STATE.ACCESS_GRANTED: [STATE.TERMINATED],
    STATE.TERMINATED: []
}

EVENT_PATTERNS = {
    Steps.DEVICE_DETECTED: [
        "Digital Key device detected",
        "Device detected",
        "BLE device detected",
    ],
    Steps.AUTH_STARTED: [
        "Session initiated",
        "Authentication started",
        "AUTH_REQUEST",
    ],
    Steps.AUTH_SUCCESS: [
        "Authentication successful",
        "AUTH_RESPONSE",
        "Authentication OK",
    ],
    Steps.RANGING_STARTED: [
        "Ranging session started",
        "UWB ranging started",
    ],
    Steps.PROXIMITY_VALIDATED: [
        "Proximity validated",
        "Distance validated",
    ],
    Steps.UNLOCK_REQUESTED: [
        "Door unlock command issued",
        "Unlock requested",
    ],
    Steps.UNLOCK_CONFIRMED: [
        "Door unlock confirmed",
        "Unlock confirmed",
    ],
    Steps.SESSION_TERMINATED: [
        "Session terminated",
        "Session terminated successfully",
    ],
}
