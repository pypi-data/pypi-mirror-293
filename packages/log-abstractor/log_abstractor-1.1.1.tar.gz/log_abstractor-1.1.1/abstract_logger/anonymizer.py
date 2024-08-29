from abc import ABC, abstractmethod
import scrubadub
class AnonymizationAdapter(ABC):
    @abstractmethod
    def anonymize(self, text: str) -> str:
        pass

class Anonymizer(AnonymizationAdapter):
    def anonymize(self, text: str) -> str:
        return scrubadub.clean(text)