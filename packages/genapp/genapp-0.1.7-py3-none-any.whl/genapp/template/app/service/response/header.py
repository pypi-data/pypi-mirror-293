from app.util import date as Dt


class HeaderKeys:
    CHANNEL = "channel"
    LANGUAGE = "language"
    VERSION = "version"
    UUID_DEVICE = "uuid_device"


class HeaderAPI:

    def __init__(
        self,
        header: dict = None,
        channel: str = None,
        language: str = None,
        version: str = None,
        uuid_device: str = None,
    ):
        if header:
            channel = header.get(HeaderKeys.CHANNEL, None)

            if channel:
                self.channel = channel

            language = header.get(HeaderKeys.LANGUAGE, None)

            if language:
                self.language = language

            version = header.get(HeaderKeys.VERSION, None)

            if version:
                self.version = version

            uuid_device = header.get(HeaderKeys.UUID_DEVICE, None)

            if uuid_device:
                self.uuid_device = uuid_device

        if channel:
            self.channel = channel

        if language:
            self.language = language

        if version:
            self.version = version

        if uuid_device:
            self.uuid_device = uuid_device

        self.timestamp = Dt.get_str_timestamp()
