from datetime import datetime

from sqlalchemy import String, DateTime, Integer, ForeignKey
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base

class LectureDB(Base):
    __tablename__ = "lectures"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(150), nullable=False)
    topic: Mapped[str | None] = mapped_column(String(50))
    content: Mapped[dict] = mapped_column(JSONB, nullable=False)


    author_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True 
    )
    
    author: Mapped["User"] = relationship(
        "User",
        back_populates="lectures",
        lazy="joined" 

    )
  

    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    

    