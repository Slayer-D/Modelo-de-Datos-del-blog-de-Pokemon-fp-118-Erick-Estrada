from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Integer, ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from enum import Enum
from sqlalchemy import Enum as SQLAEnum

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String, nullable=False)
    role: Mapped[str] = mapped_column(String, nullable=False)
    created_at: Mapped[DateTime] = mapped_column(DateTime)

    favorites: Mapped[list["Favorite"]] = relationship("Favorite", back_populates="user")

    def serialize(self):
        return {
            "id": self.id,
            "username": self.username,
            "role": self.role,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }

class Item(db.Model):
    __tablename__ = "items"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)

    favorites: Mapped[list["Favorite"]] = relationship("Favorite", back_populates="item")

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
        }

class Pokemon(db.Model):
    __tablename__ = "pokemons"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)

    favorites: Mapped[list["Favorite"]] = relationship("Favorite", back_populates="pokemon")

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
        }

class Favorite(db.Model):
    __tablename__ = "favorite"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    pokemon_id: Mapped[int] = mapped_column(ForeignKey("pokemons.id"))
    item_id: Mapped[int] = mapped_column(ForeignKey("items.id"))

    user: Mapped["User"] = relationship("User", back_populates="favorites")
    pokemon: Mapped["Pokemon"] = relationship("Pokemon", back_populates="favorites")
    item: Mapped["Item"] = relationship("Item", back_populates="favorites")

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "pokemon_id": self.pokemon_id,
            "item_id": self.item_id,
        }
