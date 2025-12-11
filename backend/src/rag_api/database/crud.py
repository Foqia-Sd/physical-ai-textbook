from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from typing import List, Optional
from ..database.models import Document, Highlight
import logging

logger = logging.getLogger(__name__)

def get_document_by_url(db: Session, url: str) -> Optional[Document]:
    """Get a document by its URL."""
    return db.query(Document).filter(Document.url == url).first()

def create_document(db: Session, url: str, title: str = None, content: str = None) -> Document:
    """Create a new document in the database."""
    try:
        # Check if document already exists
        existing_doc = get_document_by_url(db, url)
        if existing_doc:
            # Update the existing document
            existing_doc.title = title or existing_doc.title
            existing_doc.content = content or existing_doc.content
            db.commit()
            db.refresh(existing_doc)
            return existing_doc

        # Create new document
        db_document = Document(url=url, title=title, content=content)
        db.add(db_document)
        db.commit()
        db.refresh(db_document)
        return db_document
    except IntegrityError as e:
        db.rollback()
        logger.error(f"Error creating document: {e}")
        raise
    except Exception as e:
        db.rollback()
        logger.error(f"Unexpected error creating document: {e}")
        raise

def create_highlight(db: Session, document_id: int, text: str, start_char: int, end_char: int, metadata_json: str = None) -> Highlight:
    """Create a new highlight associated with a document."""
    try:
        db_highlight = Highlight(
            document_id=document_id,
            text=text,
            start_char=start_char,
            end_char=end_char,
            metadata_json=metadata_json
        )
        db.add(db_highlight)
        db.commit()
        db.refresh(db_highlight)
        return db_highlight
    except IntegrityError as e:
        db.rollback()
        logger.error(f"Error creating highlight: {e}")
        raise
    except Exception as e:
        db.rollback()
        logger.error(f"Unexpected error creating highlight: {e}")
        raise

def get_highlights_by_document(db: Session, document_id: int) -> List[Highlight]:
    """Get all highlights for a specific document."""
    return db.query(Highlight).filter(Highlight.document_id == document_id).all()

def get_all_documents(db: Session) -> List[Document]:
    """Get all documents from the database."""
    return db.query(Document).all()

def delete_document(db: Session, document_id: int) -> bool:
    """Delete a document and its associated highlights."""
    try:
        # Delete associated highlights first (due to foreign key constraint)
        db.query(Highlight).filter(Highlight.document_id == document_id).delete()

        # Delete the document
        result = db.query(Document).filter(Document.id == document_id).delete()
        db.commit()
        return result > 0
    except Exception as e:
        db.rollback()
        logger.error(f"Error deleting document: {e}")
        raise

def update_document_content(db: Session, document_id: int, content: str) -> Optional[Document]:
    """Update document content."""
    try:
        db_document = db.query(Document).filter(Document.id == document_id).first()
        if db_document:
            db_document.content = content
            db.commit()
            db.refresh(db_document)
        return db_document
    except Exception as e:
        db.rollback()
        logger.error(f"Error updating document: {e}")
        raise