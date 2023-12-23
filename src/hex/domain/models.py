from sqlmodel import SQLModel, Field


class UserBase(SQLModel):
    username: str = Field(unique=True)
