from datetime import datetime, timezone
from uuid import UUID, uuid4

from sqlalchemy import Boolean, DateTime, Float, ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import Mapped, mapped_column, relationship

from settings import Base


class Name(Base):
    __tablename__ = "names"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    name: Mapped[str] = mapped_column(String)
    request_count: Mapped[int] = mapped_column(Integer, default=0)
    last_accessed: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    predictions: Mapped[list["NameCountryPrediction"]] = relationship(back_populates="name")

    def __str__(self):
        return f"{self.name}"


class Country(Base):
    __tablename__ = "countries"

    code: Mapped[str] = mapped_column(String(2), primary_key=True)
    name: Mapped[str] = mapped_column(String)
    region: Mapped[str | None] = mapped_column(String)
    independent: Mapped[bool | None] = mapped_column(Boolean)
    google_maps: Mapped[str | None] = mapped_column(String)
    open_street_map: Mapped[str | None] = mapped_column(String)
    capital_name: Mapped[str | None] = mapped_column(String)
    capital_lat: Mapped[float | None] = mapped_column(Float)
    capital_lng: Mapped[float | None] = mapped_column(Float)
    flag_png: Mapped[str | None] = mapped_column(String)
    flag_svg: Mapped[str | None] = mapped_column(String)
    flag_alt: Mapped[str | None] = mapped_column(String)
    coat_png: Mapped[str | None] = mapped_column(String)
    coat_svg: Mapped[str | None] = mapped_column(String)
    borders: Mapped[list[str] | None] = mapped_column(ARRAY(String))

    predictions: Mapped[list["NameCountryPrediction"]] = relationship(back_populates="country")

    def __str__(self):
        return {self.code}


class NameCountryPrediction(Base):
    __tablename__ = "name_country_predictions"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    name_id: Mapped[UUID] = mapped_column(ForeignKey("names.id"))
    country_code: Mapped[str] = mapped_column(ForeignKey("countries.code"))
    probability: Mapped[float] = mapped_column(Float)

    name: Mapped["Name"] = relationship(back_populates="predictions")
    country: Mapped["Country"] = relationship(back_populates="predictions")

    __table_args__ = (UniqueConstraint("name_id", "country_code", name="_name_country_uc"),)
