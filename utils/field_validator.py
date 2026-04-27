from pydantic import BaseModel, ConfigDict, Field, PositiveInt

class UserModel(BaseModel):
    cc: PositiveInt = Field(description="The national identification of the user, and the unique identificator in the 'users' table from the database")