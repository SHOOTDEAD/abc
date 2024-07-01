import email,smtplib,time,os,random
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders


class send_mail:
    def __init__(q,senderMailid:"gmail account or yahoo account",senderSequrityCode,reciverMailid,include_time=True):
        q.senderMailid=senderMailid
        q.reciverMailid=reciverMailid
        q.senderSequrityCode=senderSequrityCode
        q.domain_map={'gmail.com':q.gmail,'yahoo.com':q.yahoo}
        q.include_time=include_time
        q.err='no error'
    
    def gmail(q):
        return smtplib.SMTP('smtp.gmail.com', 587)
    
    def yahoo(q):
        return smtplib.SMTP("smtp.mail.yahoo.com",587)
    
    def dmap(q):
        try:
            domain=q.senderMailid.split('@')[-1]
            return q.domain_map[domain]()
        except:
            print('domain_name_not_accepted')
            q.err='domain_name_not_accepted'
            return False
    def with_img(q,img_path:"path to the image",txt:str,subject='BRATZLIFE FITNESS STUDIO',web_link=None,web_info=None)->bool:
        with open(img_path, 'rb') as f:
            img_data = f.read()

        msg = MIMEMultipart()
        msg['Subject'] = subject
        msg['From'] = q.senderMailid
        msg['To'] = q.reciverMailid
        message=txt
        text = MIMEText(message)
        msg.attach(text)
        image = MIMEImage(img_data, name=os.path.basename(img_path))
        msg.attach(image)
        if q.send_it(msg):
            return True,
        return False
    
    def systime(q):
        return time.ctime(time.time())
    
    def send_it(q,msg):
        try:
            s =q.dmap()    #mapping the domain
            s.ehlo()
            s.starttls()
            s.ehlo()
            s.login(q.senderMailid, q.senderSequrityCode)
            s.sendmail(q.senderMailid, q.reciverMailid, msg.as_string())
            s.quit()
            return True
        except:
            print('error occured while sending')
            q.err='error occured while sending'
            return False
        
    def text_mail(q,subject,message,to=None):
        msg = MIMEText(message)
        msg['Subject'] = subject
        msg['From'] = q.senderMailid
        msg['To'] = to or q.reciverMailid
        if to:q.reciverMailid=to

        if q.send_it(msg):
            return True,
        return False,q.err
    
    def generate_otp(q,size:"size>5",include_alpha=False):
        if size<6:
            size=6
        s1='abcdefghijklmnopqrstuvwxyz'
        s2=s1.upper()
        n1='0987654321'
        data=n1
        if include_alpha:
            data=s1+s2+n1
        return ''.join(random.choice(data)for i in range(size))
    
    def send_file(q,file_path,subject,message):
        mes= MIMEMultipart()
        mes['From']= q.senderMailid
        mes['To']= q.reciverMailid
        mes['Subject']=subject
        mes.attach(MIMEText(message, 'plain'))
        attach_file_name=os.path.basename(file_path)
        attach_file = open(file_path, 'rb')
        payload = MIMEBase('application', 'octate-stream')
        payload.set_payload((attach_file).read())
        encoders.encode_base64(payload)
        payload.add_header('Content-Disposition', "attachment; filename= %s" % attach_file_name)
        mes.attach(payload)
        if q.send_it(mes):
            return True,
        return False,q.err    
    
BratzMail=send_mail("bratzlife999@gmail.com","tezniuttrjuleijb","lokiapm888@gmail.com")
