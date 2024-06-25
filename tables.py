import sqlite3
from sqlalchemy import create_engine, Column, Integer, String, Date, DateTime, func,BIGINT
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()


class Auth(Base):
    __tablename__="auth"
    i=Column(Integer,autoincrement=True,primary_key=True,nullable=False)
    id=Column(String(20))
    passwd=Column(String(64))
    phone=Column(BIGINT)
    def __init__ (self,id,passwd,phone):
        self.id = id
        self.passwd =passwd
        self.phone = phone
    def __repr__(self):
        return "id:%s passwd:%s phone:%s"%(self.id,self.passwd,self.phone)
    

class BasicClient(Base):
    __tablename__="basic_client_info"
    id=Column(Integer,autoincrement=True,primary_key=True,nullable=False)
    uid=Column(String(20))
    name=Column(String(80))
    email=Column(String(80))
    phone=Column(BIGINT)
    branchno=Column(Integer)
    address=Column(String(200))
    dob=Column(Date)
    height=Column(Integer)
    weight=Column(Integer)
    def __init__ (self,uid,name,email,phone,branch,address,dob,height,weight):
        self.uid = uid
        self.name = name
        self.email = email
        self.phone = phone
        self.branchno = branch
        self.address = address
        self.dob = dob
        self.height = height
        self.weight = weight
    def __repr__(self):
        return "uid%s name%s email%s phone%s branch%s address%s dob:%s height:%s weight"%(self.uid,self.name,self.email,self.phone,self.branch,self.faddress,self.dob,self.height,self.weight)


class BasicTrainer(Base):
    __tablename__="basic_trainer_info"
    id=Column(Integer,autoincrement=True,primary_key=True,nullable=False)
    ptid=Column(String(20))
    name=Column(String(80))
    email=Column(String(80))
    phone=Column(BIGINT)
    branchno=Column(Integer)
    address=Column(String(200))
    dob=Column(Date)
    height=Column(Integer)
    weight=Column(Integer)
    BaseSalary=Column(Integer)
    def __init__ (self,ptid,name,email,phone,branch,address,dob,height,weight,BaseSalary):
        self.ptid = ptid
        self.name = name
        self.email = email
        self.phone = phone
        self.branchno = branch
        self.address = address
        self.dob = dob
        self.height = height
        self.weight = weight
        self.BaseSalary = BaseSalary
    def __repr__(self):
        return "uid:%s ,name:%s,email:%s,phone:%s,branch:%s,address:%s,dob:%s,height:%s,weight:%s,BaseSalary:%s"%(self.uid,self.name,self.email,self.phone,self.branch,self.address,self.dob,self.height,self.weight,self.BaseSalary)

class PtSchedule(Base):
    __tablename__="PtSchedule"
    id=Column(Integer,autoincrement=True,primary_key=True,nullable=False)
    scheduleid=Column(String(64))
    uid=Column(String(20))
    ptid=Column(String(20))
    date=Column(Date)
    slot=Column(Integer)
    status=Column(Integer)
    def __init__(self,sid,uid,ptid,slot,date,status):
        self.scheduleid=sid
        self.uid = uid
        self.ptid = ptid
        self.slot = slot
        self.date = date
        self.status = status
    # def to(self):
    #     return str(self.uid) +str(ptid),slot,date,status
    def __repr__(self):
        return "uid:%s,ptid:%s,slot:%s,date:%s,status:%s"%(self.uid,self.ptid,self.slot,self.date,self.status)  

class PtDetails(Base):
    __tablename__="ptinfo"
    id=Column(Integer,autoincrement=True,primary_key=True,nullable=False)
    uid=Column(String(20))
    ptid=Column(String(20))
    uname=Column(String(80))
    ptname=Column(String(80))


    def __init__(self,uid,ptid,uname,ptname):
        self.ptname=ptname
        self.uid=uid
        self.ptid=ptid
        self.uname=uname


class ReschudleRequest(Base):
    __tablename__="reschedule_request"
    id=Column(Integer,autoincrement=True,primary_key=True,nullable=False)
    token=Column(String(64))
    uid=Column(String(20))
    ptid=Column(String(20))
    cdate=Column(Date)
    cslot=Column(Integer)
    rdate=Column(Date)
    rslot=Column(Integer)
    status=Column(Integer)
    to=Column(String(2))
    def __init__(self,token,uid,ptid,cslot,cdate,rslot,rdate,status,to):
        self.token = token
        self.uid = uid
        self.ptid = ptid
        self.cslot = cslot
        self.cdate = cdate
        self.rslot = rslot
        self.rdate = rdate
        self.status = status
        self.to = to
    def __repr__(self):
        return "token:%s,uid:%s,ptid:%s,cslot:%s,cdate:%s,rslot:%s,rdate:%s,status:%s,to:%s"%(self.token,self.uid,self.ptid,self.cslot,self.cdate,self.rslot,self.rdate,self.status,self.to)


# engine = create_engine("mysql+pymysql://admin:loki123@4database-1.c1u4y2eictlo.ap-south-1.rds.amazonaws.com/database-1")
# engine = create_engine(
#     host="database-1.c1u4y2eictlo.ap-south-1.rds.amazonaws.com",
#     port='3306',
#     database="database-1",
#     user="admin",
#     password="loki1234",
#     url="mysql+pymysql://"
# )
engine = create_engine("mysql+mysqldb://admin:loki1234@database-1.c1u4y2eictlo.ap-south-1.rds.amazonaws.com/gym")

Base.metadata.create_all(bind=engine)

_session = sessionmaker(bind=engine)
Session = _session()

print(222)
