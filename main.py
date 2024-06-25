from tables import Session
from fastapi import FastAPI,HTTPException
from tables import Auth,ReschudleRequest,PtSchedule,BasicClient,BasicTrainer,PtDetails
from structs import NewClient,AutoSchudle,NewTrainer,GetSchedule,FreeSlots,PlaceRequest,AcceptRequest
from datetime import datetime,timedelta
import hashlib


app=FastAPI()

def Hash(s:str):
    return hashlib.sha256(s.encode()).hexdigest()

def DateFormat(s:str):
    return datetime(*list(map(int,s.split('-')))).strftime("%Y-%m-%d")

print(DateFormat("2024-7-9")=="2024-07-9")
# @app.post("/signin")
# def signin():
#     ...


@app.get("/get_clients_details")
def get_clients_schedule():
    d=list(Session.query(BasicClient).all())
    return d
@app.get("/get_trainer_details")
def get_trainer_details():
    return list(Session.query(BasicTrainer))


@app.post("/signin",status_code=201)
def create_new_user(req:NewClient):
     d=list(Session.query(Auth.id,Auth.passwd).filter(Auth.phone==req.ph))
     print(d)
     if d :
          raise HTTPException(405,"USER ALREADY EXIST")
     uid="CT"+str(req.ph)+"@"+str(req.branchno)
     Session.add(Auth(uid,req.passwd,req.ph))
     Session.add(
          BasicClient(
               uid,
               req.name,
               req.email,
               req.ph,
               req.branchno,
               req.address,
               req.dob,
               req.height,
               req.weight
               )
            )
     Session.commit()
     return f"d REGISTERED SUCCESSFULLY {req.name}"

@app.post("/create_new_trainer",status_code=201)
def create_new_trainer(req:NewTrainer):
    d=list(Session.query(Auth.id,Auth.passwd).filter(Auth.phone==req.ph))
    if d :
        raise HTTPException(405,"USER ALREADY EXIST")
    uid="PT"+str(req.ph)+"@"+str(req.branchno)
    Session.add(Auth(uid,req.passwd,req.ph))
    Session.add(
        BasicTrainer(
            uid,
            req.name,
            req.email,
            req.ph,
            req.branchno,
            req.address,
            req.dob,
            req.height,
            req.weight,
            req.salary
            )
        )
    Session.commit()
    return f"d REGISTERED SUCCESSFULLY {req.name}"
    

@app.post("/auto_schudule",status_code=201)
def auto_schudule(req:AutoSchudle):
    req.start_date=DateFormat(req.start_date)
    l=dict()
    for i,j in Session.query(PtSchedule.slot,PtSchedule.date).filter(PtSchedule.ptid==req.ptid,PtSchedule.date>=req.start_date):
        if j.strftime("%Y-%m-%d") in l:
            l[j.strftime("%Y-%m-%d")].append(i)
        else:
            l[j.strftime("%Y-%m-%d")]=[i]
    slots=[]
    i=0
    # print(l)
    while len(slots)<req.no_session:
        date=datetime(*list(map(int,req.start_date.split("-"))))+timedelta(i)
        # print("qwerty",l[date.strftime("%Y-%m-%d")])
        if date.strftime("%Y-%m-%d") in l:
            if len(l[date.strftime("%Y-%m-%d")])==13:
                i+=1
                continue
            # print("qwer",l[date.strftime("%Y-%m-%d")])
            slot={1,2,3,4,5,6,7,8,9,10,11,12,13}-set(l[date.strftime("%Y-%m-%d")])
            # print(slot)
            st=slot.pop()
            s=PtSchedule(
            Hash( 
                date.strftime("%Y-%m-%d")+str(st)+req.ptid),
                req.uid,
                req.ptid,
                st,
                date.strftime("%Y-%m-%d"),
                0
            )
            slots.append(s)
            i+=1
            continue
        s=PtSchedule(
            Hash(date.strftime("%Y-%m-%d")+str(1)+req.ptid),
            req.uid,
            req.ptid,
            1,
            date.strftime("%Y-%m-%d"),
            0
            )
        slots.append(s)
        i+=1
    ptDetails=Session.query(PtDetails.uname).filter(PtDetails.uid==req.uid).all()
    
    if not ptDetails:
        uname=list(Session.query(BasicClient.name).filter(BasicClient.uid==req.uid))[0][0]
        ptname=list(Session.query(BasicTrainer.name).filter(BasicTrainer.ptid==req.ptid))[0][0]
        print(uname,ptname)
        Session.add(PtDetails(req.uid,req.ptid,uname,ptname))
    Session.bulk_save_objects(slots)
    Session.commit()
    return slots
     

@app.get("/get_pt_client_details")
def get_pt_client_details():
    l=[]
    for uid,ptid,ptname,uname in Session.query(PtDetails.uid,PtDetails.ptid,PtDetails.ptname,PtDetails.uname).all():
        l.append({
            "USER_NAME":uname,
            "PT_NAME":ptname,
            "slot":list(Session.query(PtSchedule.date,PtSchedule.slot).filter(PtSchedule.uid==uid,PtSchedule.ptid==ptid))
            }
        )
    return l

@app.get("/get_pt_client_details_without_slots")
def get_pt_client_details_without_slots():
    return list(Session.query(PtDetails))

@app.post("/get_schedule")
def get_schedule(req:GetSchedule):
    if req.date:
        return list(Session.query(PtSchedule.slot,PtSchedule.scheduleid).filter(PtSchedule.date==req.date,PtSchedule.ptid==req.id))
    return list(Session.query(PtSchedule.date,PtSchedule.slot,PtSchedule.scheduleid).filter(PtSchedule.uid==req.id))

@app.post("/request_free_slots")
def request_free_slots(req:FreeSlots):
    req.to_date=DateFormat(req.to_date)
    PtScheduleData=list(Session.query(PtSchedule.ptid).filter(PtSchedule.scheduleid==req.c_schudleid))
    if not PtScheduleData:
        raise HTTPException(405,"CURRENT-PT session id is Invalid")
    ptid=PtScheduleData[0][0]
    x=lambda x:x[0]
    l=set(map(x,Session.query(PtSchedule.slot).filter(PtSchedule.date==req.to_date,PtSchedule.ptid==ptid)))
    print(l)
    return {"free_slots":{1,2,3,4,5,6,7,8,9,10,11,12,13}-l}

@app.post("/place_request")
def place_request(req:PlaceRequest):
    req.to_date=DateFormat(req.to_date)
    to="CT"
    if req.id[:2]=="CT":
        to="PT"
    cur_date=datetime.now().strftime("%Y-%m%-d")
    PtScheduleData=list(Session.query(PtSchedule.uid,PtSchedule.ptid,PtSchedule.date,PtSchedule.slot).filter(PtSchedule.scheduleid==req.c_scheduleid,PtSchedule.date>=cur_date))
    if not PtScheduleData:
        raise HTTPException(405,"CURRENT-PT session id is Invalid")
    uid,ptid,c_date,c_slot=PtScheduleData[0][0],PtScheduleData[0][1],PtScheduleData[0][2],PtScheduleData[0][3]
    retoken=Hash(req.to_date+str(req.to_slot)+ptid)
    print(80)
    # if list(Session.query(PtSchedule.date)).filter
    # print(list(Session.query(ReschudleRequest.token).filter(ReschudleRequest.token==retoken)))

    #checks slot is occupied or not
    print(list(Session.query(PtSchedule.date).filter(PtSchedule.scheduleid==retoken)))
    if list(Session.query(PtSchedule.date).filter(PtSchedule.scheduleid==retoken)):
        raise HTTPException(403,"Requested Session Already Booked by someone else")
    
    #checks req slot is requested by someone else or not
    if list(Session.query(ReschudleRequest.token).filter(ReschudleRequest.token==retoken)):
        raise HTTPException(403,"Requested Session Engagend Plese Choose any other slot")
    x=lambda x:x[0]
    l=set(map(x,Session.query(PtSchedule.slot).filter(PtSchedule.date==req.to_date,PtSchedule.ptid==ptid)))
    print(90)
    print(l,req.to_slot,l.issuperset({req.to_slot}))
    if l.issuperset({req.to_slot}):
        raise HTTPException(403,"Requested Session Already Booked by someone else")
    Session.add(ReschudleRequest(retoken,uid,ptid,c_slot,c_date,req.to_slot,req.to_date,10,to)) #10=>requested ,20=>Rejected,30>Accepted
    Session.commit()
    return f"Request for rescheduling of PT on Date: {req.to_date} Slot: {req.to_slot} had been placed successfully"

@app.get("/request_status")
def request_status(id:str):
    print(list(Session.query(Auth).filter(Auth.id==id)))
    if not list(Session.query(Auth).filter(Auth.id==id)):
        raise HTTPException(403,"USER NOT EXIST")
    if id[:2]=="CT":
        return list(
            Session.query(ReschudleRequest).filter(ReschudleRequest.uid==id,ReschudleRequest.cdate>=datetime.now().strftime("%Y-%m-%d"))
            )
    if id[:2]=="PT":
        return list(
            Session.query(ReschudleRequest).filter(ReschudleRequest.ptid==id,ReschudleRequest.cdate>=datetime.now().strftime("%Y-%m-%d"))
            )
    return "invalid"

@app.post("/accept_request",status_code=202)
def accept_request(req:AcceptRequest):
    d={"CT":"PT","PT":"CT"}
    if req.id[:2]!="CT" and req.id[:2]!="PT":
        raise HTTPException(400,f"plese cross check the id {req.id}")
    if not list(Session.query(Auth).filter(Auth.id==req.id)):
        raise HTTPException(404,f"USER {req.id} NOT FOUND")
    
    if not list(Session.query(PtSchedule.status).filter(PtSchedule.scheduleid==req.c_scheduleid,PtSchedule.date>=datetime.now().strftime("%Y-%m-%d"))):
        raise HTTPException(404,f"CURRENT SLOT ID IS INVAID{req.c_scheduleid}")
    query_data=list(
        Session.query(
            ReschudleRequest.token,
            ReschudleRequest.uid,
            ReschudleRequest.ptid,
            ReschudleRequest.rslot,
            ReschudleRequest.rdate,
            ReschudleRequest.status,
            ReschudleRequest.to
        ).filter(ReschudleRequest.token==req.rescheduleid)
        )
    print(query_data)
    if not query_data:
        raise HTTPException(405,f"CURRENT SCHUDLE ID {req.c_scheduleid} IS INVALID")
    if query_data[0][-1]!=req.id[:2]:
        raise HTTPException(401,"YOU DOND HAVE CREADENTIALS")
    print(query_data)
    if query_data[0][-2]!=10:
        raise HTTPException(403,"REQUEST HAVE ALREADY PRROCESSED")
    if req.status==20:
        Session.query(ReschudleRequest).filter(ReschudleRequest.token==req.rescheduleid).update({"status":20})
        Session.commit()
        return f"REQUESTED SLOT{query_data[0]} IS SUCCESSFULLY REJECTED"
    if req.status==30:
        Session.query(ReschudleRequest).filter(ReschudleRequest.token==req.rescheduleid).update({"status":30})
        Session.add(PtSchedule(*query_data[0][:-2]))
        Session.delete(PtSchedule(scheduleid=req.c_scheduleid))
        Session.commit()
        return f"ACCEPTED THE REQUESTED SLOT{query_data[0][3]} ON {query_data[0][4]}"
    return f"GIVEN STATUS CODE{query_data[0[-2]]} IS IN VALID"
    # Session.delete(PtSchedule(scheduleid=req.rescheduleid))
    