DB_EXTENSION = 'sqlite3'

class SmartPadalaOutlet:
    def __init__(self, outlet_num: str, address: str, service_fee: float) -> None:
        self.outlet_number = outlet_num
        self.address = address
        self.service_fee = service_fee


SMART_PADALA_OUTLETS = [
    SmartPadalaOutlet(
        outlet_num="005-008-2002",
        address="123 Sample Street Sample City",
        service_fee=50,
    ),
    SmartPadalaOutlet(
        outlet_num="005-016-2001",
        address="246 Foo Street Foo City",
        service_fee=30,
    ),
    SmartPadalaOutlet(
        outlet_num="006-006-2003",
        address="369 Bar Street Bar City",
        service_fee=40,
    ),
    SmartPadalaOutlet(
        outlet_num="009-019-2001",
        address="481 Baz Street Baz City",
        service_fee=80,
    ),
    SmartPadalaOutlet(
        outlet_num="002-021-2000",
        address="510 Peter Street Peterson City",
        service_fee=60,
    ),
]
