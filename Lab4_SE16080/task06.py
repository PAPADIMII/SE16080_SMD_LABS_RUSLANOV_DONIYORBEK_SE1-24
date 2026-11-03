# Task 6 — Duck typing and Protocol
# export_report needs only a write(bytes) method returning the number of bytes.
import io
from typing import Protocol

class Writable(Protocol):
    def write(self, data: bytes) -> int: ...

def export_report(rows, target: Writable) -> None:
    for row in rows:
        target.write((",".join(map(str, row)) + "\n").encode())

class S3Upload:
    def __init__(self, bucket, key):
        self.bucket, self.key = bucket, key
        self.parts = []
    def write(self, data: bytes) -> int:
        self.parts.append(data)
        return len(data)

class FakeWriter:
    def __init__(self):
        self.data = bytearray()
    def write(self, data: bytes) -> int:
        self.data.extend(data)
        return len(data)

def test_export_targets():
    rows = [["name", "age"], ["Ali", 20]]
    expected = b"name,age\nAli,20\n"

    buffer = io.BytesIO()
    export_report(rows, buffer)
    assert buffer.getvalue() == expected

    s3 = S3Upload("reports", "students.csv")
    export_report(rows, s3)
    assert b"".join(s3.parts) == expected

    fake = FakeWriter()
    export_report(rows, fake)
    assert bytes(fake.data) == expected

# A target without write() fails when export_report tries to call target.write().
# mypy can detect a statically typed incompatible target before execution.
