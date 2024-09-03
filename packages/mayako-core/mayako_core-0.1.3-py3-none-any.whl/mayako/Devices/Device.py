from ..Utils.Identity import Identity

class Device:

    identity: str
    description: str

    def __init__(self, identity: str, description: str = "") -> None:
        Identity.register(identity)
        self.identity = identity
        self.description = description