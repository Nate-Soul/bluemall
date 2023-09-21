import sys


from paypalcheckoutsdk.core import PayPalHttpClient, SandboxEnvironment


class PayPalClient:
    def __init__(self):
        self.client_id     = 'ASBAk99GQYzaijFgpfAxfqTGpE14F2RsPhg-HkGGSAyfG6A9q_osK7cF6PQQrQYVHV9D-8Gvj9eO-6sn'
        self.client_secret = 'EAKf36Vh7BZBm3XeIXDDuLNBO8LfkDp8Dww9aiSJyO_EdlijepCKt9tIcxkSuZP_pvEHsjw5VpFsBrU4'
        self.environment   = SandboxEnvironment(client_id=self.client_id, client_secret=self.client_secret)
        self.client        = PayPalHttpClient(self.environment)
