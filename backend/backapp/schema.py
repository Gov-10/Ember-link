from ninja import Schema
from typing import Optional
class ProfileSchema(Schema):
   phone:str
   location:Optional[str]=None
   role:str