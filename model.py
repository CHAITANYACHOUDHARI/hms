import pymysql as pm


class Database:
    def __init__(self):
        self.conn = pm.connect(host="remotemysql.com", user="0p80GrC8yz", password="C3cdXHW2HS", database="0p80GrC8yz")
        self.cursor = self.conn.cursor()

    # Checking Admin Login
    def getAdminData(self, username, password):
        query = "select * from adminlogin where username='%s' and password='%s'" % (username, password)
        status = self.cursor.execute(query)
        if self.cursor.rowcount > 0:
            status = True
            admininfo = self.cursor.fetchone()

            # sending status and data to submitadmindata (email,name)
            return status, admininfo

        else:
            status = False
            return (status)


    def setPatientAppointment(self, name, age, gender, ailment, mobile, address, dr, date, slot):
        self.cursor.execute("select * from `appointment-table` where id like 'oid%'")
        count = self.cursor.rowcount
        oid = 'oid' + str(count + 1)

        self.cursor.execute(
            "INSERT INTO `appointment-table`(`id`, `name`, `age`, `gender`, `ailment`, `contact-no`, `address`, `select-dr`,`schedule`, `slot`) VALUES('%s', '%s', %d , '%s', '%s', '%s', '%s', '%s', '%s','%s')" % (
            oid, name, age, gender, ailment, mobile, address, dr, date, slot))
        try:
            self.conn.commit()
            status = (True , oid)

        except:
            self.conn.rollback()
            status = False

        return status


    def submitPatientLogin(self, username, passw):  # model for patient login
        self.query = "select * from patient where (email='%s' or pid='%s') and password='%s'" % (username,username, passw)  # database entry
        self.cursor.execute(self.query)
        if self.cursor.rowcount > 0:
            self.status = True
        else:
            self.status = False
        return self.status


    def submitMrAppointment(self, name, company, mobile, doctor, schedule):  # model for mr appointment
        self.cursor.execute("insert into `mr-appointment` values('%s','%s','%s','%s','%s')" % (
            name, company, mobile, doctor, schedule))  # database entry
        try:
            self.conn.commit()
            self.status = True
        except:
            self.conn.rollback()
            self.status = False
        return self.status


    def setcontactdata(self, name, email, subject, message):  # model for contact
        self.cursor.execute(
            "INSERT INTO `contact-us`(`name`, `email-id`, `subject`, `message`) VALUES('%s' ,'%s' ,'%s' ,'%s')" % (
                name, email, subject, message))  # database entry

        try:
            self.conn.commit()
            status = True

        except:
            self.conn.rollback()
            status = False
        return status


    # patient signup
    def setsignupdata(self, name, dateofbirth, gender, email, mobileno, address, password):
        self.cursor.execute('select * from patient')
        count = self.cursor.rowcount
        pid = 'pid' + str(count + 1)

        self.cursor.execute("insert into patient values('%s','%s','%s','%s','%s','%s','%s','%s')" % (
            pid, name, dateofbirth, gender, email, mobileno, address, password))

        try:
            # if error occur here try block will not execute and except block will execute
            self.conn.commit()
            status = (True , pid)

        except:
            self.conn.rollback()
            status = False
        return status


    # doctor login
    def submitDoctorLogin(self, username, password):
        query = "select * from doctorinfo where (did='%s' or email='%s') and password='%s'" % (
            username, username, password)
        self.cursor.execute(query)
        if self.cursor.rowcount > 0:
            status = True
        else:
            status = False
        return status


        # Room Available Form
    def getroomavailabledata(self, room):
        # Query For room available
        self.cursor.execute("SELECT `available` FROM `room-available` WHERE rtype='%s'" % (room))
        if self.cursor.rowcount > 0:
            self.available = self.cursor.fetchone()
            self.conn.commit()
        else:
            self.available = -1
        return (self.available)


    def getPatientId(self):
        self.cursor.execute('select * from `medical-cert`')
        count = self.cursor.rowcount
        pid = 'pid'+str(count+1)
        return pid

    # Store Medical Certificate
    def setCertificate(self, patientname, doctorname, disease, reason, date):

        self.cursor.execute(
            "INSERT INTO `medical-cert`(`name`, `sel-dr`, `diagnosis`, `reason`, `date`) VALUES ('%s','%s','%s','%s','%s')" % (
            patientname, doctorname, disease, reason, date))

        try:
            self.conn.commit()
            status = True

        except:
            self.conn.rollback()
            status = False
        return status


    # change password
    def setPassword(self,oldpassw,passw,username):  # change password

        self.cursor.execute("select * from adminlogin where username='%s' and password='%s'" % (username,oldpassw))

        if self.cursor.rowcount > 0:
            self.cursor.execute("update adminlogin set password='%s' where username='%s'"% (passw,username))  # database entry
            try:
                self.conn.commit()
                status = True
            except:
                self.conn.rollback()
                status = False
        else:
            status = False
        return status


    # changes to do                 | changes done by | date        | description
    # storing discharge form data   |   Rutik         | 26-05-21    | updating payee,payment and discharge_date
    # checking admit data           |                 |             |


    def getAutofillData(self,pid):
        self.cursor.execute("select * from patient where pid='%s'" % (pid))

        if self.cursor.rowcount > 0:
            status = True
            data = self.cursor.fetchone()
        else:
            status = False
            data = None
        return  status,data


    def getTemporaryId(self):
        self.cursor.execute('select * from `admit-discharge`')
        count = self.cursor.rowcount
        id = "TID"+str(count+1)
        return id


    def setAdmitData(self,id,name,age,gender,disease,mobile,doctor,admit_date,address):
        query = "insert into `admit-discharge` (`id`,`name`,`age`,`gender`,`disease`,`mob`,`address`,`sel-dr`,`doa`) values('%s','%s',%d,'%s','%s','%s','%s','%s','%s')" % (id,name,age,gender,disease,mobile,address,doctor,admit_date)
        self.cursor.execute(query)

        try:
            self.conn.commit()
            status = True

        except:
            self.conn.rollback()
            status = False

        return status


    # this method checks if id exist in admit_discharge Table
    def getAdmitData(self,id):
        self.cursor.execute("select * from `admit-discharge` where id='%s'" % (id))
        if self.cursor.rowcount > 0:
            status = True
            data = self.cursor.fetchone()
        else:
            status = False
            data = None
        return  status,data


    # stores discharge data in database
    def setDischargeData(self,id,name, mobile, discharge_date, payee, payment):
        self.cursor.execute("update `admit-discharge` set amt='%s',payee = '%s', dod='%s' where name = '%s' and mob = '%s' and id='%s'" % (payment,payee,discharge_date,name,mobile,id))
        try:
            self.conn.commit()
            status = True
        except:
            self.conn.rollback()
            status = False
        return status

# >>>>>>>>>>>>>>>>>>>>>>>>>End of Code (Rutik)<<<<<<<<<<<<<<<<<<<<<<


    def getDoctorId(self):
        self.cursor.execute('select * from `doctorinfo`')
        count = self.cursor.rowcount
        did = 'did'+str(count+1)
        return did

    def adddoctor(self,did,name,qualification,major,dob,gender,email,mobile,address,passw):
        self.cursor.execute("insert into doctorinfo values ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')"%(did,name,qualification,gender,major,dob,email,mobile,address,passw))
        try:
            self.conn.commit()
            status = True
        except:
            self.conn.rollback()
            status = False
        return status

        # Remove Doctor
    def removedoctor(self, DID, email, username, password):
        self.cursor.execute("select * from adminlogin where username='%s' and password='%s'" % (username, password))
        if self.cursor.rowcount > 0:
            delete = self.cursor.execute("delete from doctorinfo where did='%s' and email='%s'" % (DID, email))
            if(delete!=False):
                self.conn.commit()
                status = True
            else:
                self.conn.rollback()
                status = False
            return status
        else:
            return False


    # Chaitanya (code for opd patient appointment)

    def setpatientdata(self, pid, name, age, gender, ailment, mob, address, doctor, schedule_date,
                       slot):  # defining function
        self.cursor.execute(
            "insert into `appointment-table` values('%s','%s',%d,'%s','%s','%s','%s','%s','%s','%s')" % (
            pid, name, age, gender, ailment, mob, address, doctor, schedule_date,
            slot))  # insert values of respective fields in table appointment-table
        try:
            self.conn.commit()
            status = True
        except:
            self.conn.rollback()
            status = False
        return status



    #Chaitanya PatientHome Appointment
    def fetchData(self, username):  # function to fetch data from patient table to appointment table
        self.cursor.execute("select pid,name,dob,gender,mob,address from patient where pid='%s' or email='%s'" % (
        username,username))  # query to fetch respective data from patient table  where pid or email= data stored in session variable
        if self.cursor.rowcount > 0:  # takes count of row
            data = self.cursor.fetchone()  # automatically fetch entry of first row(pid here) and store it in variable 'data'.fetchone(). Fetches the next row (case) from the active dataset. The result is a single tuple
            pid = data[0]  # this is to access data
            name = data[1]  # seperately from tuple
            date = data[2]
            date = str(date)
            yob = date[0:4]
            yob = int(yob)
            gender = data[3]
            mob = data[4]
            address = data[5]
            return (pid, name, yob, gender, mob, address)




    # To get Feedback data for admin --Ritik
    def getFeedbackData(self):
        self.cursor.execute('select * from `contact-us`')
        feedback = self.cursor.fetchall()
        return feedback
    
    #To get Appointment data for admin --Lakhan
    def getAdminAppointment(self,date):
        date=str(date)
        self.cursor.execute("select name,`select-dr`,schedule,slot from `appointment-table` where schedule='%s'"%(date))
        appoint = self.cursor.fetchall()
        return appoint

        # Raghvendra 28/05/2021 22:00 hrs ---
        # To get Appointment data for doctor

    def getDoctorAppointment(self, date, username):
        date = str(date)
        self.cursor.execute("select name from doctorinfo where email='%s' or did='%s'" % (username, username))
        data = self.cursor.fetchone()
        name = data[0]
        self.cursor.execute("select name, ailment, schedule, slot from `appointment-table` where schedule='%s' and `select-dr`='%s'" % (date, name))
        appointdoctor = self.cursor.fetchall()
        return appointdoctor

        # Raghvendra 28/05/2021 22:00 hrs ---
        # To get Appointment data for patient

    def getPatientAppointment(self, username):

        self.cursor.execute("select name from patient where (email='%s' or pid='%s')" % (username, username))
        data = self.cursor.fetchone()
        name = data[0]
        print(data)
        self.cursor.execute("select `select-dr`, ailment, schedule, slot from `appointment-table` where `name`='%s'" % (name))
        appointpatient = self.cursor.fetchall()
        return appointpatient

    # Gunjan patient change password

    def setPatientPassword(self,oldpassw,passw,username):

        self.cursor.execute("select * from patient where (email='%s' or pid='%s') and password='%s'" % (username,username,oldpassw))

        if self.cursor.rowcount > 0:
            passwchange = self.cursor.execute("update patient set password='%s' where (email='%s' or pid='%s')" % (passw, username,username))  # database entry

            if(passwchange):
                self.conn.commit()
                status = True
            else:
                self.conn.rollback()
                status = False
        else:
            status = False

        return status

    # Gunjan doctor change password

    def setDoctorPassword(self, oldpassw, passw, username):
        self.cursor.execute('select * from `doctorinfo` where (did="%s" or email="%s") and password ="%s"' %(username,username,oldpassw))

        if self.cursor.rowcount > 0:
            passwChange = self.cursor.execute("update doctorinfo set password='%s' where (email='%s' or did='%s')" % (passw, username,username))  # database entry

            if(passwChange):
                self.conn.commit()
                status = True
            else:
                self.conn.rollback()
                status = False
        else:
            status = False

        return status
    
    #  update doctor info(chaitanya)
    
    def takeData(self,username):                 #function to fetch and autofill the previous data
        self.cursor.execute("select did,name,qualification,gender,major,dob,email,mob,address from doctorinfo where did='%s' or email='%s'" % (username,username))  # query to fetch respective data from doctor info  where pid or email= data stored in session variable
        if self.cursor.rowcount > 0:                     
            data = self.cursor.fetchone()      # automatically fetch entry of first row(pid here) and store it in variable 'data'.fetchone(). Fetches the next row (case) from the active dataset. The result is a single tuple   
            return (data)
     #Raghvendra changed name
    def UpdateDoctorInfo(self,name,qualification,gender,major,dob,email,mob,address,username) :                 #function for storing and update data

        self.cursor.execute("update doctorinfo set name='%s',qualification='%s',gender='%s',major='%s',dob='%s',email='%s',mob='%s',address='%s' where did='%s' or email='%s'" % (name,qualification,gender,major,dob,email,mob,address,username,username))
        try:
            # if error occur here try block will not execute and except block will execute
            self.conn.commit()
            status = True

        except:
            self.conn.rollback()
            status = False
        return status

    # update patient info (samiksha)

    def tookData(self, username):
        self.cursor.execute("select pid,name,dob,gender,email,mob,address from patient where pid='%s' or email='%s'" % (
            username,
            username))  # query to fetch respective data from patient table  where pid or email= data stored in session variable
        if self.cursor.rowcount > 0:
            data = self.cursor.fetchone()
            return (data)

    def UpdatePtInfo(self, name, dob, gender, email, mob, address, username):
        self.cursor.execute(
            "update patient set name='%s',dob='%s',gender='%s',email='%s',mob='%s',address='%s' where pid='%s' or email='%s'" % (
            name, dob, gender, email, mob, address, username, username))
        try:
            # if error occur here try block will not execute and except block will execute
            self.conn.commit()
            status = True
        except:
            self.conn.rollback()
            status = False
        return status


