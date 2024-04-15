from typing import Optional, List

from sqlalchemy import String, Integer, ForeignKey, Date, BigInteger
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db import Base


class Client(Base):
    __tablename__ = "clients"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    account_number: Mapped[BigInteger] = mapped_column(
        BigInteger, unique=True, index=True
    )
    surname: Mapped[str] = mapped_column(String, index=True)
    name: Mapped[str] = mapped_column(String, index=True)
    middle_name: Mapped[str] = mapped_column(String, index=True)
    birth_date: Mapped[Date] = mapped_column(Date, index=True)
    # ИНН — индивидуальный номер налогоплательщика, ITN — Individual Taxpayer Number
    itn: Mapped[BigInteger] = mapped_column(BigInteger, index=True)
    status: Mapped[str] = mapped_column(String, index=True, default="not_at_work")
    responsible_user_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("users.id"), index=True
    )
