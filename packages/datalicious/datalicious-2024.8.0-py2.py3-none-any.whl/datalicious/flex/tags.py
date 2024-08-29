import struct
from enum import Enum
from decimal import Decimal

from dataclasses import dataclass


class VA:
    """
    >>> VA.from_tag(b'VA   0   56914716650144959952130 ')
    VA(turnover=56914716650, time=Time(microsecond=53399952130))
    """

    __slots__ = "turnover", "time"
    ID = "VA"

    def __init__(self, turnover, time):
        self.turnover = turnover
        self.time = time

    def __repr__(self):
        return f"VA(turnover={self.turnover}, time={self.time!r})"

    @classmethod
    def from_tag(cls, tag_information):
        (
            tag_id,
            _,
            _,
            unit_flag,
            turnover_value,
            time,  # HHMMSStttttt
            _,
        ) = struct.unpack("2s2scc14s12sc", tag_information)
        turnover = int(turnover_value) * 10 ** int(unit_flag)
        return cls(turnover, Time.from_flex(time))


class VL:
    """
    >>> VL.from_tag(b'VL   0      95380000144959952130 ')
    VL(volume=95380000, time=Time(microsecond=53399952130))
    """

    __slots__ = "volume", "time"
    ID = "VL"

    def __init__(self, volume, time):
        self.volume = volume
        self.time = time

    def __repr__(self):
        return f"VL(volume={self.volume}, time={self.time!r})"

    @classmethod
    def from_tag(cls, tag_information):
        (
            tag_id,
            _,
            _,
            unit_flag,
            trading_volume,
            time,  # HHMMSStttttt
            _,
        ) = struct.unpack("2s2scc14s12sc", tag_information)
        turnover = int(trading_volume) * 10 ** int(unit_flag)
        return cls(turnover, Time.from_flex(time))


class PR:
    """PRice because 1P is not valid Python
    >>> PR.from_tag(b'1P  3       5962000+1450002629903   ')
    PR(price=Decimal('596.2'), change=<Change.SAME: 3>, time=Time(microsecond=53400262990))
    """

    __slots__ = "price", "change", "time"
    ID = "1P"

    def __init__(self, price, change, time):
        self.price = price
        self.change = change
        self.time = time

    def __repr__(self):
        return f"PR(price={self.price!r}, change={self.change!r}, time={self.time!r})"

    @classmethod
    def from_tag(cls, tag_information):
        (
            tag_id,
            _,
            unit_flag,
            integral,
            decimal,
            sign,
            time,  # HHMMSStttttt
            change_flag,
            stq_reference_point_flag,
            _,
            closing_price_input,
        ) = struct.unpack("2s2sc10s4sc12scccc", tag_information)
        price = price_from(unit_flag, integral, decimal, sign)
        try:
            change = Change(int(change_flag))
        except ValueError:
            change = Change.REFRESH
        return cls(price, change, Time.from_flex(time))


def price_from(unit_flag, integral, decimal, sign):
    if unit_flag == b" ":
        return None
    if unit_flag == b"4":
        decimal = 0
    else:
        decimal = int(decimal[: -int(unit_flag)])
    price = Decimal(f"{int(integral)}.{decimal}")
    return price


class Change(Enum):
    UP = 1
    DOWN = 2
    SAME = 3
    OTHER = 4
    REFRESH = " "


class NO:
    """
    >>> NO.from_tag(b'NO  614944    1    1    0')
    NO(update_no=614944, packet_sno=1, number_of_packets=1, divided_message_sno=0)
    """

    __slots__ = "update_no", "packet_sno", "number_of_packets", "divided_message_sno"
    ID = "NO"

    def __init__(self, update_no, packet_sno, number_of_packets, divided_message_sno):
        self.update_no = update_no
        self.packet_sno = packet_sno
        self.number_of_packets = number_of_packets
        self.divided_message_sno = divided_message_sno

    def __repr__(self):
        return f"NO(update_no={self.update_no}, packet_sno={self.packet_sno}, number_of_packets={self.number_of_packets}, divided_message_sno={self.divided_message_sno})"

    @classmethod
    def from_tag(cls, tag_information):
        (
            tag_id,
            update_no,
            packet_sno,
            total_number_of_packet_sno,
            divided_message_sno,
        ) = struct.unpack("2s8s5s5s5s", tag_information)
        try:
            divided_message_sno = int(divided_message_sno)
        except ValueError:
            divided_message_sno = "E"
        return cls(
            int(update_no),
            int(packet_sno),
            int(total_number_of_packet_sno),
            divided_message_sno,
        )


class ST:
    """
    >>> ST.from_tag(b'ST   20  0123000031214    ')
    ST(change=False, status=20, state=b'  ', short_regulation=True, time=Time(microsecond=45000031214))
    """

    __slots__ = "change", "status", "state", "short_regulation", "time"
    ID = "ST"

    def __init__(self, change, status, state, short_regulation, time):
        self.change = change
        self.status = status
        self.state = state
        self.short_regulation = short_regulation
        self.time = time

    def __repr__(self):
        return f"ST(change={self.change}, status={self.status}, state={self.state}, short_regulation={self.short_regulation}, time={self.time!r})"

    @classmethod
    def from_tag(cls, tag_information):
        (
            tag_id,
            _,
            change_flag,
            issue_status,
            state_flag,
            short_selling_regulation_flag,
            time,
            _,
        ) = struct.unpack("2s2sc2s2sc12s4s", tag_information)
        try:
            change = bool(int(change_flag))
        except ValueError:
            change = False
        return cls(
            change,
            int(issue_status),
            state_flag,
            bool(short_selling_regulation_flag),
            Time.from_flex(time),
        )


class Q:

    __slots__ = "side", "price", "volume", "orders", "middle", "time"

    def __init__(self, side, price, volume, orders, middle, time):
        self.side = side
        self.price = price
        self.volume = volume
        self.orders = orders
        self.middle = middle
        self.time = time

    @property
    def market(self):
        return self.price == Decimal("0.0")

    @classmethod
    def from_tag(cls, tag_information):
        (
            tag_id,
            _,
            change_flag,
            price_unit_flag,
            integral,
            decimal,
            sign,
            time,
            quote_flag,
            matching_sign,
            volume_unit_flag,
            quantity,
            sign,
            number_unit_flag,
            number,
            sign,
            middle_of_book_flag,
        ) = struct.unpack("2s2scc10s4sc12sccc14scc14scc", tag_information)
        middle = bool(int(middle_of_book_flag))
        side = TAGID_TO_SIDE[tag_id]
        try:
            volume = int(quantity) * 10 ** int(volume_unit_flag)
        except ValueError:
            volume = 0
        try:
            orders = int(number) * 10 ** int(number_unit_flag)
        except ValueError:
            orders = 0
        price = price_from(price_unit_flag, integral, decimal, sign)
        # market order
        if price is None:
            price = Decimal("0.0")
        return cls(side, price, volume, orders, middle, Time.from_flex(time))

    def __repr__(self):
        return f"{self.ID}(side='{self.side}', price={self.price!r}, volume={self.volume}, orders={self.orders}, middle={self.middle}, time={self.time!r})"


TAGID_TO_SIDE = {
    b"QB": "B",
    b"QS": "S",
    b"SC": "S",
    b"BC": "B",
}


class QB(Q):
    """
    >>> QB.from_tag(
    ...     b'QB  13       5961000+145000224720100         37400+0            19+0'
    ... )
    QB(side='B', price=Decimal('596.1'), volume=37400, orders=19, middle=False, time=Time(microsecond=53400224720))
    >>> QB.from_tag(
    ...     b'QB  13       5155000+080000096901 0                                1'
    ... )
    QB(side='B', price=Decimal('515.5'), volume=0, orders=0, middle=True, time=Time(microsecond=28800096901))
    """

    ID = "QB"


class QS(Q):
    """
    >>> QS.from_tag(
    ...     b'QS  13       5963000+145000228488100         20600+0            14+1'
    ... )
    QS(side='S', price=Decimal('596.3'), volume=20600, orders=14, middle=True, time=Time(microsecond=53400228488))
    """

    ID = "QS"


class C:

    __slots__ = "side", "price", "volume", "orders", "time"
    close = True

    def __init__(self, side, price, volume, orders, time):
        self.side = side
        self.price = price
        self.volume = volume
        self.orders = orders
        self.time = time

    @property
    def market(self):
        return self.price == Decimal("0.0")

    @classmethod
    def from_tag(cls, tag_information):
        (
            tag_id,
            _,
            change_flag,
            price_unit_flag,
            integral,
            decimal,
            sign,
            time,
            _,
            volume_unit_flag,
            quantity,
            sign,
            number_unit_flag,
            number,
            sign,
        ) = struct.unpack("2s2scc10s4sc12scc14scc14sc", tag_information)
        side = TAGID_TO_SIDE[tag_id]
        try:
            volume = int(quantity) * 10 ** int(volume_unit_flag)
        except ValueError:
            volume = 0
        try:
            orders = int(number) * 10 ** int(number_unit_flag)
        except ValueError:
            orders = 0
        price = price_from(price_unit_flag, integral, decimal, sign)
        # market order
        if price is None:
            price = Decimal("0.0")
        return cls(side, price, volume, orders, Time.from_flex(time))

    def __repr__(self):
        return f"{self.ID}(side='{self.side}', price={self.price!r}, volume={self.volume}, orders={self.orders}, time={self.time!r})"


class SC(C):
    """
    >>> SC.from_tag(
    ...     b'SC  1                145000119158 0       2678900+0           234+'
    ... )
    SC(side='S', price=Decimal('0.0'), volume=2678900, orders=234, time=Time(microsecond=53400119158))
    """

    ID = "SC"


class BC(C):
    """
    >>> BC.from_tag(
    ...     b'BC  1                145000012200 0       3611600+0           218+'
    ... )
    BC(side='B', price=Decimal('0.0'), volume=3611600, orders=218, time=Time(microsecond=53400012200))

    """

    ID = "BC"


@dataclass(order=True, unsafe_hash=True)
class Time:
    """JST time - microsecond from midnight

    >>> Time.from_flex(b'144959952130') < Time.from_time(15)
    True
    >>> Time.from_time(14, 50) - Time.from_time(14, 49, 59)
    1000000
    >>> Time.from_flex(b'144959952130')
    Time(microsecond=53399952130)
    >>> print(Time.from_flex(b'144959952130'))
    14:49:59.952130
    """

    microsecond: int

    @classmethod
    def from_flex(cls, timestamp):
        try:
            hh, mm, ss, tttttt = map(int, struct.unpack("2s2s2s6s", timestamp))
        except ValueError:
            microsecond = 0
        else:
            microsecond = (((hh * 60) + mm) * 60 + ss) * 1000000 + tttttt
        return cls(microsecond)

    @classmethod
    def from_time(cls, hh, mm=0, ss=0, tttttt=0):
        microsecond = (((hh * 60) + mm) * 60 + ss) * 1000000 + tttttt
        return cls(microsecond)

    def __str__(self):
        more, tttttt = divmod(self.microsecond, 1000000)
        more, SS = divmod(more, 60)
        HH, MM = divmod(more, 60)
        return f"{HH:0>2}:{MM:0>2}:{SS:0>2}.{tttttt:0>6}"

    def __sub__(self, other):
        return self.microsecond - other.microsecond

    def __add__(self, other):
        return Time(self.microsecond + other)
