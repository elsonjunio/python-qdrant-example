from abc import ABC, abstractmethod
from typing import List
from PyPDF2 import PdfReader
import speech_recognition as sr
from pathlib import Path
from .models import Document


class BaseExtractor(ABC):
    """Abstract base class for document extractors.

    Provides the interface for all concrete extractor implementations that
    handle different file formats.
    """

    @abstractmethod
    def extract(self, file_path: str) -> List[Document]:
        """Extracts text content from a file and returns structured documents.

        Args:
            file_path: Path to the input file to be processed

        Returns:
            List of Document objects containing extracted content and metadata

        Raises:
            NotImplementedError: Must be implemented by concrete subclasses
            FileNotFoundError: If the input file doesn't exist
            ValueError: If the file content cannot be processed
        """
        pass


class PDFExtractor(BaseExtractor):
    """Extracts text content from PDF documents while preserving page structure."""

    def extract(self, file_path: str) -> List[Document]:
        """Processes a PDF file and extracts text with page-level granularity.

        Args:
            file_path: Path to the PDF file to be processed

        Returns:
            List of Document objects, one for each non-empty page

        Example:
            >>> extractor = PDFExtractor()
            >>> documents = extractor.extract("document.pdf")
            >>> len(documents)  # Returns number of pages with content
            15

        Note:
            Empty pages are automatically filtered out from the results.
        """
        reader = PdfReader(file_path)
        documents = []

        for page_number, page in enumerate(reader.pages, start=1):
            text = page.extract_text()
            if text.strip():
                documents.append(
                    Document(
                        content=text,
                        metadata={'source': Path(file_path).name},
                        page_number=page_number,
                    )
                )

        return documents


class AudioExtractor(BaseExtractor):
    """Extracts text content from audio files using speech recognition."""

    def __init__(self):
        """Initializes the speech recognition engine."""
        self.recognizer = sr.Recognizer()

    def extract(self, file_path: str) -> List[Document]:
        """Transcribes speech content from audio files to text.

        Args:
            file_path: Path to the audio file (WAV, MP3, OGG)

        Returns:
            List with a single Document object containing the full transcription,
            or empty list if recognition fails

        Example:
            >>> extractor = AudioExtractor()
            >>> documents = extractor.extract("recording.wav")
            >>> if documents:
            ...     print(documents[0].content)  # Prints transcribed text

        Note:
            Uses Google's speech recognition API (requires internet connection).
            Currently configured for Portuguese language (pt-BR).
        """
        with sr.AudioFile(file_path) as source:
            audio = self.recognizer.record(source)

            try:
                text = self.recognizer.recognize_google(
                    audio, language='pt-BR'
                )
                return [
                    Document(
                        content=text,
                        metadata={'source': Path(file_path).name},
                        page_number=None,
                    )
                ]
            except sr.UnknownValueError:
                print('Audio could not be understood')
                return []
            except sr.RequestError:
                print('Speech recognition service error')
                return []


def get_extractor(file_extension: str) -> BaseExtractor:
    """Factory function that provides the appropriate extractor for a file type.

    Args:
        file_extension: File extension including dot (e.g. '.pdf', '.mp3')

    Returns:
        Concrete BaseExtractor instance for the specified file type

    Raises:
        ValueError: If no extractor is available for the given extension

    Example:
        >>> extractor = get_extractor('.pdf')  # Returns PDFExtractor instance
        >>> audio_extractor = get_extractor('.wav')  # Returns AudioExtractor
    """
    if file_extension.lower() == '.pdf':
        return PDFExtractor()
    elif file_extension.lower() in ['.wav', '.mp3', '.ogg']:
        return AudioExtractor()
    else:
        raise ValueError(f'No extractor available for {file_extension} files')
