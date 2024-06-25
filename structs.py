from pydantic import BaseModel,EmailStr

class NewClient(BaseModel):
    ph:int
    name:str
    email:EmailStr
    address:str
    branchno:int
    dob:str
    height:int
    weight:int
    passwd:str

class AutoSchudle(BaseModel):
    uid:str
    ptid:str
    no_session:int
    start_date:str

class NewTrainer(BaseModel):
    ph:int
    name:str
    email:EmailStr
    address:str
    branchno:int
    dob:str
    height:int
    weight:int
    passwd:str
    salary:int


class GetSchedule(BaseModel):
    id:str
    date:str =None

class FreeSlots(BaseModel):
    to_date:str
    c_schudleid:str   

class PlaceRequest(BaseModel):
    id:str
    c_scheduleid:str
    to_date:str
    to_slot:int

class AcceptRequest(BaseModel):
    id:str
    c_scheduleid:str
    rescheduleid:str
    status:int
    
