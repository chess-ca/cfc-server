
import re, zipfile as zf


class SimpleZipFile:
    def __init__(self, file_name: str):
        self.file_name = file_name
        self.error = None
        self.exception = None
        self.names = []
        try:
            with zf.ZipFile(file_name, mode='r') as zip_f:
                self.names = zip_f.namelist()
        except FileNotFoundError as e:
            self.error = 'file-not-found'
            self.exception = e
        except zf.BadZipfile as e:
            self.error = 'bad-zip-file'
            self.exception = e

    def is_valid(self) -> bool:
        return self.error is None

    def get_error(self, raise_exception=False) -> str:
        if raise_exception:
            raise self.exception
        return self.error

    def has_name(self, name: str) -> bool:
        return name in self.names

    def matching_names(self, pattern: str, flags=0) -> list:
        p = re.compile(pattern, flags)
        return [n for n in self.names if p.match(n)]

    def get_bytes(self, name: str) -> bytes:
        with zf.ZipFile(self.file_name, mode='r') as zip_file:
            if name not in zip_file.namelist():
                m_bytes = b''
            else:
                with zip_file.open(name) as zip_member:
                    m_bytes = zip_member.read()
        return m_bytes

    def get_contents(self, name, encoding='utf8') -> str:
        return self.get_bytes(name).decode(encoding)

    def multi_get_contents(self, pattern: str, flags=0, encoding='utf8'):
        names = self.matching_names(pattern, flags)
        with zf.ZipFile(self.file_name, mode='r') as zip_file:
            for name in names:
                with zip_file.open(name) as zip_member:
                    m_bytes = zip_member.read()
                    yield name, m_bytes.decode(encoding)
