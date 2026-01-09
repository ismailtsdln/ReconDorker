import pikepdf
import docx
import httpx
import os
from .utils import setup_logging

logger = setup_logging()

class MetadataExtractor:
    @staticmethod
    async def extract_from_url(url, client=None):
        """Downloads a file and extracts metadata based on extension."""
        if not any(url.lower().endswith(ext) for ext in ['.pdf', '.docx']):
            return None
            
        try:
            if client:
                response = await client.get(url, timeout=10.0)
            else:
                async with httpx.AsyncClient() as c:
                    response = await c.get(url, timeout=10.0)
            
            response.raise_for_status()
            temp_file = "temp_meta_file"
            with open(temp_file, "wb") as f:
                f.write(response.content)
            
            metadata = {}
            if url.lower().endswith('.pdf'):
                metadata = MetadataExtractor.extract_pdf(temp_file)
            elif url.lower().endswith('.docx'):
                metadata = MetadataExtractor.extract_docx(temp_file)
            
            os.remove(temp_file)
            return metadata
        except Exception as e:
            logger.error(f"Metadata extraction error for {url}: {e}")
            return None

    @staticmethod
    def extract_pdf(filepath):
        try:
            with pikepdf.open(filepath) as pdf:
                meta = pdf.docinfo
                return {str(k): str(v) for k, v in meta.items()}
        except:
            return {}

    @staticmethod
    def extract_docx(filepath):
        try:
            doc = docx.Document(filepath)
            prop = doc.core_properties
            return {
                "author": prop.author,
                "created": str(prop.created),
                "last_modified_by": prop.last_modified_by,
                "title": prop.title
            }
        except:
            return {}
