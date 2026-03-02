from sqlalchemy import Column, ForeignKey, Integer, Text
from sqlalchemy.orm import relationship

from .db import Base


class Paper(Base):
    __tablename__ = "papers"

    id = Column(Text, primary_key=True)
    source = Column(Text)
    publication = Column(Text)
    title = Column(Text)
    authors = Column(Text)
    abstract = Column(Text)
    doi = Column(Text, nullable=True)
    year = Column(Integer)
    published_date = Column(Text, nullable=True)
    xplore_url = Column(Text)
    pdf_url = Column(Text, nullable=True)
    is_oa = Column(Integer, default=0)
    keywords = Column(Text)
    created_at = Column(Text)
    updated_at = Column(Text)

    summary = relationship("Summary", back_populates="paper", uselist=False)


class Summary(Base):
    __tablename__ = "summaries"

    id = Column(Text, primary_key=True)
    paper_id = Column(Text, ForeignKey("papers.id"), unique=True)
    provider = Column(Text)
    model = Column(Text)
    summary_json = Column(Text)
    summary_md = Column(Text)
    tokens_in = Column(Integer, nullable=True)
    tokens_out = Column(Integer, nullable=True)
    created_at = Column(Text)

    paper = relationship("Paper", back_populates="summary")


class Swipe(Base):
    __tablename__ = "swipes"

    id = Column(Text, primary_key=True)
    paper_id = Column(Text, ForeignKey("papers.id"))
    decision = Column(Text)
    notes = Column(Text, nullable=True)
    tags = Column(Text, nullable=True)
    swiped_at = Column(Text)


class Job(Base):
    __tablename__ = "jobs"

    id = Column(Text, primary_key=True)
    type = Column(Text)
    status = Column(Text)
    total = Column(Integer, default=0)
    done = Column(Integer, default=0)
    error = Column(Text, nullable=True)
    created_at = Column(Text)
    updated_at = Column(Text)
