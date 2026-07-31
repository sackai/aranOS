from datetime import datetime
from pydantic import BaseModel, EmailStr, Field
class UserCreate(BaseModel):
    email: EmailStr
    full_name: str = Field(min_length=2)
    password: str = Field(min_length=8)
class UserRead(BaseModel):
    id: int; email: EmailStr; full_name: str; created_at: datetime
    model_config = {"from_attributes": True}
class UserLogin(BaseModel):
    email: EmailStr
    password: str
class Token(BaseModel):
    access_token: str; token_type: str = "bearer"; user: UserRead
class ProjectCreate(BaseModel):
    name: str = Field(min_length=2); idea: str = Field(min_length=10)
class AgentRead(BaseModel):
    id: int; role: str; prompt: str; memory: dict; output: str; status: str; position: int
    model_config = {"from_attributes": True}
class LogRead(BaseModel):
    id: int; agent_id: int | None; message: str; level: str; created_at: datetime
    model_config = {"from_attributes": True}
class ProjectRead(BaseModel):
    id: int; name: str; idea: str; status: str; generated_files: dict; documentation: str; created_at: datetime; updated_at: datetime; agents: list[AgentRead] = []; logs: list[LogRead] = []
    model_config = {"from_attributes": True}
