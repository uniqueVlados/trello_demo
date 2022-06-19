from sqlalchemy import Column, Integer, ForeignKey, String, Date, Boolean, Text
from .database import Base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func


class Board(Base):
    __tablename__ = "board"
    id = Column(Integer, nullable=False, unique=True, primary_key=True, autoincrement=True)
    title = Column(String(20))

    tasks = relationship("Task", back_populates="board", cascade="all, delete")

    def __repr__(self):  # Перегрузка текстового представления
        return f"<Board({self.id},{self.title})>"


class Task(Base):
    __tablename__ = "task"

    id = Column(Integer, nullable=False, unique=True, primary_key=True, autoincrement=True)
    text = Column(String(50))
    is_complete = Column(Boolean, default=False)
    board_id = Column(Integer, ForeignKey("board.id", ondelete="CASCADE"), nullable=False)
    date_created = Column(Date(), default = func.now())

    board = relationship("Board", back_populates="tasks", uselist=False)

    def __repr__(self):
        return f"<Task({self.id},{self.text})>"
