#copied source file from ev3dev micropython: https://github.com/pybricks/debian-pybricks-micropython3/blob/ev3dev-stretch/bricks/ev3dev/modules/pybricks/messaging.py
#changed so not only names but mac-addresses can be used too
from _thread import allocate_lock
from uerrno import ECONNRESET
from ustruct import pack, unpack

from pybricks.bluetooth import (
    resolve,
    BDADDR_ANY,
    ThreadingRFCOMMServer,
    ThreadingRFCOMMClient,
    StreamRequestHandler,
)


class Mailbox:
    def __init__(self, name, connection, encode=None, decode=None):
        self.name = name
        self._connection = connection

        if encode:
            self.encode = encode

        if decode:
            self.decode = decode

    def encode(self, value):
        return value

    def decode(self, payload):
        return payload

    def read(self):
        """Reads the current value of the mailbox.

        Returns:
            The decoed value or ``None`` if the mailbox has never received
            a value.
        """
        data = self._connection.read_from_mailbox(self.name)
        if data is None:
            return None
        return self.decode(data)

    def send(self, value, destination=None):
        """Sends a value to remote mailboxes with the same name as this
        mailbox.

        Arguments:
            value: The value to send.
            destination: The name or address of a specific device or ``None``
                to broadcast to all connected devices.
        """
        data = self.encode(value)
        self._connection.send_to_mailbox(destination, self.name, data)

    def wait(self):
        """Waits for the mailbox to receive a message."""
        self._connection.wait_for_mailbox_update(self.name)

    def wait_new(self):
        """Waits for the mailbox to receive a message that is different from
        the current contents of the mailbox.

        Returns:
            The new value. (Same as return value of :meth:`read`.)
        """
        old = self.read()
        while True:
            self.wait()
            new = self.read()
            if new != old:
                return new


class LogicMailbox(Mailbox):
    def encode(self, value):
        return b"\x01" if value else b"\x00"

    def decode(self, payload):
        return bool(payload[0])


class NumericMailbox(Mailbox):
    """:class:`Mailbox` that holds a numeric or floating point value.

    This is compatible with the "numeric" message blocks in the standard
    EV3 firmware.
    """

    def encode(self, value):
        return pack("<f", value)

    def decode(self, payload):
        return unpack("<f", payload)[0]


class TextMailbox(Mailbox):
    """:class:`Text` that holds a text or string point value.

    This is compatible with the "text" message blocks in the standard
    EV3 firmware.
    """

    def encode(self, value):
        return "{}\0".format(value)

    def decode(self, payload):
        return payload.decode().strip("\0")


# EV3 standard firmware is hard-coded to use channel 1
EV3_RFCOMM_CHANNEL = 1

# EV3 VM bytecodes
SYSTEM_COMMAND_NO_REPLY = 0x81
WRITEMAILBOX = 0x9E


class MailboxHandler(StreamRequestHandler):
    def handle(self):
        with self.server._lock:
            self.server._clients[self.client_address[0]] = self.request
        while True:
            try:
                buf = self.rfile.read(2)
            except OSError as ex:
                # The client disconnected the connection
                if ex.errno == ECONNRESET:
                    break
                raise
            (size,) = unpack("<H", buf)
            buf = self.rfile.read(size)
            msg_count, cmd_type, cmd, name_size = unpack("<HBBB", buf)
            if cmd_type != SYSTEM_COMMAND_NO_REPLY:
                raise ValueError("Bad message type")
            if cmd != WRITEMAILBOX:
                raise ValueError("Bad command")
            mbox = buf[5 : 5 + name_size].decode().strip("\0")
            (data_size,) = unpack("<H", buf[5 + name_size : 7 + name_size])
            data = buf[7 + name_size : 7 + name_size + data_size]

            with self.server._lock:
                self.server._mailboxes[mbox] = data
                update_lock = self.server._updates.get(mbox)
                if update_lock:
                    update_lock.release()


class MailboxHandlerMixIn:
    def __init__(self):
        # protects against concurrent access of other attributes
        self._lock = allocate_lock()
        # map of mailbox name to raw data
        self._mailboxes = {}
        # map of device name/address to object with send() method
        self._clients = {}
        # map of mailbox name to mutex lock
        self._updates = {}
        # map of names to addresses
        self._addresses = {}

    def read_from_mailbox(self, mbox):
        with self._lock:
            return self._mailboxes.get(mbox)

    def send_to_mailbox(self, brick, mbox, payload):
        mbox_len = len(mbox) + 1
        payload_len = len(payload)
        send_len = 7 + mbox_len + payload_len
        fmt = "<HHBBB{}sH{}s".format(mbox_len, payload_len)
        data = pack(
            fmt,
            send_len,
            1,
            SYSTEM_COMMAND_NO_REPLY,
            WRITEMAILBOX,
            mbox_len,
            mbox,
            payload_len,
            payload,
        )
        with self._lock:
            if brick is None:
                for client in self._clients.values():
                    client.send(data)
            else:
                addr = self._addresses.get(brick)
                if addr is None:
                    addr = resolve(brick)
                    self._addresses[brick] = addr
                if addr is None:
                    raise ValueError('no paired devices matching "{}"'.format(brick))
                self._clients[addr].send(data)

    def wait_for_mailbox_update(self, mbox):
        lock = allocate_lock()
        lock.acquire()
        with self._lock:
            self._updates[mbox] = lock
        try:
            return lock.acquire()
        finally:
            with self._lock:
                del self._updates[mbox]


class BluetoothMailboxServer(MailboxHandlerMixIn, ThreadingRFCOMMServer):
    def __init__(self):
        super().__init__()
        super(ThreadingRFCOMMServer, self).__init__(
            (BDADDR_ANY, EV3_RFCOMM_CHANNEL), MailboxHandler
        )

    def wait_for_connection(self, count=1):
        for _ in range(count):
            self.handle_request()


class MailboxRFCOMMClient(ThreadingRFCOMMClient):
    def __init__(self, parent, bdaddr):
        self.parent = parent
        super().__init__((bdaddr, EV3_RFCOMM_CHANNEL), MailboxHandler)

    def send(self, data):
        self.socket.send(data)

    def finish_request(self, request, client_address):
        self.RequestHandlerClass(request, client_address, self.parent)


class BluetoothMailboxClient(MailboxHandlerMixIn):
    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self.close()

    def connect(self, brick):
        addr = resolve(brick)
        try:
            if addr is None and not brick[2] == ":" and not ":" == brick[5] and not ":" == brick[8] and not ":" == brick[11] and not ":" == brick[13]:
                raise ValueError('no paired devices matching "{}"'.format(brick))
            else:
                if addr == None: addr = brick
        except IndexError: pass

        client = MailboxRFCOMMClient(self, addr)
        if self._clients.setdefault(addr, client) is not client:
            raise ValueError("connection with this address already exists")
        try:
            client.handle_request()
        except:
            del self._clients[addr]
            raise

    def close(self):
        for client in self._clients.values():
            client.client_close()
        self._clients.clear()
        #https://github.com/pybricks/pybricks-projects/blob/master/tutorials/wireless/hub-to-hub/broadcast/vehicle.py
