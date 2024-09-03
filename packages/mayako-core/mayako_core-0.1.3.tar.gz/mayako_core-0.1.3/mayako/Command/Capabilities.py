from .BaseCommand import BaseCommand
from typing import TYPE_CHECKING

# To avoid cyclic import errors while still being able to use a class as a type
if TYPE_CHECKING:
    from ..Utils.Record import Record

#directly export as dict with enum

class RecordRead(BaseCommand):

    def __init__(self, record: Record) -> None:
        super().__init__()
        self.record = record

    def execute(self) -> None:
        self.record._read()

class RecordCreate(BaseCommand):

    def __init__(self, record: Record) -> None:
        super().__init__()
        self.record = record

    def execute(self) -> None:
        self.record._create()

class RecordStart(BaseCommand):

    def __init__(self, record: Record) -> None:
        super().__init__()
        self.record = record

    def execute(self) -> None:
        self.record._start()

class RecordStop(BaseCommand):

    def __init__(self, record: Record) -> None:
        super().__init__()
        self.record = record

    def execute(self) -> None:
        self.record._stop()