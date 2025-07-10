from sqlmodel import Field, SQLModel


class ModelTest(SQLModel, table=True):
    """Test model for API testing."""

    __table_args__ = {"extend_existing": True}

    id: int = Field(primary_key=True)
    name: str = Field()
    description: str = Field()
