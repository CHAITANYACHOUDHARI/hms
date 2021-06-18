# changes to do:-      |   changes done by   |  date:-    | Description:-
# Added Comments       |   Lakhan            | 26-May-21  | Added comments part at the begining 
#  Admin page          |   Gunjan            |26-may-21|  |#change password , medical certificate         
# Doctor and patient   |  Gunjan             | 27-may-21  |  password change
# updatePatientInfo    | Samiksha            | 28-May-21  | Autofill  UpdatePatientInfo

# added function       |  Raghvendra         |  16:00 hrs | added function to update doctor info,
# UpdateDoctorInfo     |                     | 29/05/2021 | to show appointments in admin,patient and doctor home
# getpatientappointment|                     |            | fixed change password bug, and some other minor bugs
# getdoctorappointment |                     |            |
# getadminappointment  |  Raghvendra         |            |


from flask import Flask, render_template, request, session, redirect
from model import Database
from datetime import date, datetime

app = Flask(__name__)
app.secret_key = "abcd"


# Page Routes


# Index Route
@app.route('/')
def index():
    return render_template('index.html')


# Aboutus Route
@app.route('/aboutus')
def aboutus():
    return render_template('aboutus.html')


# Contactus Route
@app.route('/contactus')
def contactus():
    return render_template('contactus.html')


# Patient Login Route
@app.route('/patientlogin')
def patientlogin():
    return render_template('patientlogin.html')


# Pateint Signup Route
@app.route('/patientsignup')
def patientsignup():
    return render_template('patientsignup.html')


# Doctor Login Route
@app.route('/doctorlogin')
def doctorlogin():
    return render_template('doctorlogin.html')


# Admin Login Route
@app.route('/adminLoginPage')
def adminLoginPage():
    return render_template('adminlogin.html')


# OPD Appointment Route
@app.route('/opdAppointmentForm')
def opdAppointmentForm():
    return render_template('opdappointmentform.html')


# MR Apoinntment Route
@app.route('/mrappointment')  # page route for patient login failed
def mrappointment():
    return render_template('mrappointment.html')


# Room Availability Route
@app.route('/roomavailability')
def roomavailability():
    return render_template('roomavailability.html')


# ---------------------Page Route End-------------------------------
# *********************Ppge Route End*******************************


# Patient Home
@app.route('/patienthome')
def patienthome():
    return render_template('patienthome.html')


@app.route('/doctorthome')
def doctorhome():
    return render_template('doctorhome.html')

@app.route('/adminhome')
def adminhome():
    return render_template('adminhome.html')


#  ****  END OF PAGE ROUTES  ****

# **** FORM ROUTES ****

# *** HOME PAGE FORMS ***

# Patient SignUp
@app.route('/submitPatientSignup', methods=['POST', 'GET'])
def submitPatientSignup():
    if request.method == 'POST':
        name = request.form['name']
        dateofbirth = request.form['dob']
        gender = request.form['gender']
        email = request.form['email']
        mobileno = request.form['mobile']
        address = request.form['address']
        password = request.form['passw']
        confirmpassword = request.form['cpassw']

        if password == confirmpassword:
            obj = Database()
            status = obj.setsignupdata(name, dateofbirth, gender, email, mobileno, address, password)

            if status[0] == True:
                return render_template('patientsignup.html', msg="SignUpSuccess",pid=status[1])
            else:
                return  render_template('patientsignup.html',msg="SignUpFailed")
        else:
            return render_template('patientsignup.html', msg="SignUpFailed")


# Updated updatePatientInfo # editied by samiksha 

@app.route('/submitPatientLogin', methods=['POST', 'GET'])  # action route for patient login to patienthome
def submitPatientLogin():
    if request.method == 'POST':
        username = request.form['username']
        passw = request.form['passw']
        db = Database()
        if db.submitPatientLogin(username, passw) == True:
            session['username'] = username  # session storing username
            data = db.tookData(username)  # fetching data using function fetchdata defined in model.py                                       #date of birth

            session['data'] = data

            appointpatient = db.getPatientAppointment(username)
            session['login'] = True
            session['loginuser'] = 'patient'
            session['appointpatient'] = appointpatient
            session['appointlen'] = len(appointpatient)

            return render_template('patienthome.html', msg="loginSuccess")
        else:
            return render_template("patientlogin.html", msg="loginFailed")



# Doctor Login
@app.route('/submitDoctorLogin', methods=['GET', 'POST'])
def submitDoctorLogin():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['passw']
        obj = Database()

        if obj.submitDoctorLogin(username, password) == True:
            session['username'] = username
            obj = Database()
            data = obj.takeData(username)  # fetching data using function fetchdata defined in model.py                                       #date of birth

            session['data'] = data

            # Raghvendra 28/05/2021 22:00 hrs
            todays_date = date.today()
            appointdoctor = obj.getDoctorAppointment(todays_date, username)
            session['appointdoctor'] = appointdoctor
            session['appointlen'] = len(appointdoctor)
            session['login'] = True
            session['loginuser'] = 'doctor'
            return render_template('doctorhome.html', msg="loginSuccess")
        else:
            return render_template('doctorlogin.html', msg='loginFailed')


# Admin Login
@app.route('/submitAdminLogin', methods=['POST', 'GET'])
def submitAdminLogin():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['passw']

        db = Database()
        status = db.getAdminData(username, password)

        feedbackdata = db.getFeedbackData()
        #Lakhan Appointment Data
        todays_date = date.today()
        appointdata=db.getAdminAppointment(todays_date)

        if status:
            # Taking data from database
            session['name'] = status[1][1]
            session['email'] = status[1][2]
            session['feedback'] = feedbackdata
            session['len'] = len(feedbackdata)
            session['appointdata'] = appointdata
            session['appointlen'] = len(appointdata)
            session['login'] = True
            session['loginuser'] = 'admin'

            return render_template('adminhome.html', msg="loginSuccess")

        else:
            return render_template('adminlogin.html', msg="loginFailed")


# Patient Appointment
@app.route('/submitPatientAppointment', methods=['POST', 'GET'])
def submitPatientAppointment():
    if request.method == 'POST':
        name = request.form['name']
        age = int(request.form['age'])
        gender = request.form['gender']
        ailment = request.form['ailment']
        mobile = request.form['mobile']
        address = request.form['address']
        doctor = request.form['doctor']
        schedule_date = request.form['schedule_date']
        schedule_time = request.form['schedule_time']

        obj = Database()
        status= obj.setPatientAppointment(name, age, gender, ailment, mobile, address, doctor, schedule_date,
                                           schedule_time)

        if status[0] == True:
            return render_template('opdappointmentform.html', msg="success",oid=status[1])
        else:
            return render_template('opdappointmentform.html', msg="failed")


# MR Appointment
@app.route('/submitMrAppointment', methods=['POST', 'GET'])  # action route for mr-appointment
def submitMrAppointment():
    if request.method == 'POST':
        name = request.form['name']
        company = request.form['company']
        mobile = request.form['mobile']
        doctor = request.form['doctor']
        schedule = request.form['schedule_date']
        db = Database()
        if db.submitMrAppointment(name, company, mobile, doctor, schedule) == True:
            session['name'] = name
            return render_template('mrappointment.html', msg="mrAppointmentSuccess")
        else:
            return render_template("mrappointment.html", msg="mrAppointmentFailed")


# Contact Us
@app.route('/submitContactUs', methods=['GET', 'POST'])  # action route for contact
def submitContactUs():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        subject = request.form['subject']
        message = request.form['message']
        obj = Database()
        status = obj.setcontactdata(name, email, subject, message)
        if status == True:
            return render_template('contactus.html', msg="Thank you")
        else:
            return render_template('contactus.html', msg="Try again leater")


# Room Availability
@app.route('/checkRoomAvailability', methods=['GET', 'POST'])
def checkRoomAvailability():  # Function fo Route
    if request.method == 'POST':
        room = request.form['room_type']
        obj = Database()
        # Calling object
        available = obj.getroomavailabledata(room)
        # Returning Available rooms to roomavailability.html through available variable
        return render_template('roomavailability.html', available=available)
        # Print the available using jinja in roomavailability.html file


# *** END OF HOME PAGE FORMS ***

# *** ADMIN HOME PAGE FORMS ***

# Autofill in Admit Form(adminhome.html)
@app.route('/autofillAdmitForm', methods=['GET', 'POST'])
def autofillAdmitForm():
    if request.method == 'POST':
        pid = request.form['pid']

        db = Database()
        status, data = db.getAutofillData(pid)

        if status:
            age = str(int(date.today().year) - int(str(data[2])[:4]))

            return render_template('adminhome.html', msg="autofillsuccess", admit_name=data[1], admit_age=age,
                                   gender=data[3], email=data[4], admit_mobile=data[5], admit_address=data[6], id=pid)
        else:
            return render_template('adminhome.html', msg="autofillfailed")


# Admit Form (adminhome.html)
@app.route('/submitAdmitForm', methods=['GET', 'POST'])
def submitAdmitForm():
    if request.method == 'POST':
        name = request.form['name']
        age = int(request.form['age'])
        gender = request.form['gender']
        disease = request.form['disease']
        mobile = request.form['mobile']
        doctor = request.form['doctor']
        admit_date = request.form['admit_date']
        address = request.form['address']

        db = Database()

        # In case patient dont have signup account(PID) except block will execute
        try:
            id = request.form['id']
        except:
            # gives temporary id for non-registered patients(who dont have pid)
            id = db.getTemporaryId()

        status = db.setAdmitData(id, name, age, gender, disease, mobile, doctor, admit_date, address)

        if status:
            return render_template('adminhome.html', msg="admitformsuccess", id=id)
        else:
            return render_template('adminhome.html', msg='admitformfailed')


# changes to do:            | changes done by | date:-      | description :-
# handeling discharge form  |   Rutik         | 26-05-21    |


# Auto filling Discharge form
@app.route('/checkAdmitId', methods=['GET', 'POST'])
def checkAdmitId():
    if request.method == 'POST':
        id = request.form['id']
        db = Database()
        status, data = db.getAdmitData(id)

        if status:
            id = data[0]
            name = data[1]
            doctor = data[7]
            disease = data[4]
            mobile = data[5]
            admit_date = str(data[8])[:10]
            admit_date = datetime.strptime(admit_date, '%Y-%m-%d').date()

            return render_template('adminhome.html', msg="dischargeIdSuccess", id=id, name=name, doctor=doctor,
                                   disease=disease, mobile=mobile, admit_date=admit_date)

        else:
            return render_template('adminhome.html', msg="autofillfailed")


# Handling Discharge form
@app.route('/submitDischargeForm', methods=['GET', 'POST'])
def submitDischargeForm():
    if request.method == 'POST':
        id = request.form['id']
        name = request.form['name']
        doctor = request.form['doctor']
        disease = request.form['disease']
        mobile = request.form['mobile']
        admit_date = request.form['admit_date']
        discharge_date = request.form['discharge_date']
        payee = request.form['payee']
        payment = request.form['payment']

        # As we have only one table for both admit and discharge
        # we have to only update the data and parameteres like name,admit_date,doctor,disease,mobile
        # are already there in table
        # hence we are sending only name and mobile number to chcck the row
        # and discharge_date,payee and payment to update the row

        db = Database()
        status = db.setDischargeData(id, name, mobile, discharge_date, payee, payment)

        if status:
            # need to change render path here
            # thinking about adding payment receipt
            return render_template('temp.html', msg="dischargeSuccess",id=id, name=name, mobile=mobile, discharge_date=discharge_date, payee=payee, payment=payment)
        else:
            return render_template('adminhome.html', msg='dischargeFailed')


# Admin Password Change
# change password
@app.route('/changePassword', methods=['GET', 'POST'])
def changePassword():
    if request.method == 'POST':
        oldpassw = request.form['oldpassw']
        passw = request.form['passw']
        cpassw = request.form['cpassw']
        if passw == cpassw:
            obj = Database()
            username = session['email']
            status = obj.setPassword(oldpassw, passw, username)
            if status:
                return render_template('adminhome.html', msg="passwordChangeSuccess")
            else:
                return render_template('adminhome.html', msg='passwordChangeFailed')
        else:
            return render_template('adminhome.html', msg='passwordNotMatched')


# Admin Logout
@app.route('/adminLogout', methods=["GET", "POST"])
def adminLogout():
    session['email'] = ""
    session['name'] = ""
    session['len'] = 0
    session['appointlen'] = ""
    session['feedback'] = ""
    session['appointdata'] = ""
    session['login'] = False
    session['loginuser'] = ''
    return redirect('/')


@app.route('/logoutDoctor', methods=["GET", "POST"])
def logoutDoctor():
    session['username'] = ""
    session['login'] = False
    session['loginuser'] = ''

    return redirect('/')


@app.route('/logoutPatient', methods=["GET", "POST"])
def logoutPatient():
    session['username'] = ""
    session['login'] = False
    session['loginuser'] = ''

    return redirect('/')



# medical certificate
@app.route('/medicalCertificate', methods=['GET', 'POST'])
def medicalCertificate():
    if request.method == 'POST':
        patientname = request.form['patientname']
        doctorname = request.form['doctorname']
        disease = request.form['disease']
        reason = request.form['reason']
        date = request.form['date']
        obj = Database()

        if obj.setCertificate(patientname, doctorname, disease, reason, date) == True:

            return render_template('adminhome.html', msg="medCertSuccess")
        else:
            return render_template('adminhome.html', msg="medCertFailed")


# Add Doctor to Database
@app.route('/adddoctor', methods=['GET', 'POST'])
def adddoctor():
    if request.method == 'POST':
        name = request.form['name']
        qualification = request.form['qualification']
        major = request.form['major']
        dob = request.form['dob']
        gender = request.form['gender']
        email = request.form['email']
        mobile = request.form['mobile']
        address = request.form['address']
        passw = request.form['passw']
        cpassw = request.form['cpassw']
        if passw == cpassw:
            obj1 = Database()
            did = obj1.getDoctorId()
            obj = Database()
            if obj.adddoctor(did, name, qualification, major, dob, gender, email, mobile, address, passw) == True:
                return render_template('adminhome.html', msg='addDoctorSuccess', did=did)
        else:
            return render_template('adminhome.html', msg='addDoctorPasswordFailed')
    return render_template('adminhome.html', msg='addDoctorFailed')


# Remove Doctor Form
@app.route('/removedoctor', methods=['GET', 'POST'])
def removedoctor():
    if request.method == 'POST':
        DID = request.form['DID']
        email = request.form['email']
        password = request.form['password']
        username = session['email']
        obj = Database()
        if obj.removedoctor(DID, email, username, password) == True:
            return render_template('adminhome.html', msg='removeDoctorSuccess')
        else:
            return render_template('adminhome.html', msg='removeDoctorFailed')


# ADMIN HOME END
# PATIENT HOME

@app.route('/MakeAnAppointment', methods=['GET', 'POST'])
def MakeAnAppointment():
    if request.method == 'POST':
        ailment = request.form['ailment']
        doctor = request.form['doctor']
        schedule_date = request.form['schedule_date']
        slot = request.form['schedule_time']
        username = session['username']  # to store session data in variable username
        obj = Database()

        pid, name, yob, gender, mob, address = obj.fetchData(
            username)  # fetching data using function fetchdata.defined in model.py
        todays_date = date.today()  # to calculate age
        currentYear = int(todays_date.year)  # using
        age = currentYear - yob  # date of birth

        status = obj.setpatientdata(pid, name, age, gender, ailment, mob, address, doctor, schedule_date,
                                    slot)  # calling function setpatientdata
        if status == True:
            db = Database()
            appointpatient = db.getPatientAppointment(username=pid)
            session['appointpatient'] = appointpatient
            session['appointlen'] = len(appointpatient)
            return render_template('patientHome.html', msg="appointmentSuccess")
        else:
            return render_template('patientHome.html', msg="appointmentFailed")


# @app.route('/temp')
# def temp():
#     return render_template('temp.html')


# *** END OF ADMIN HOME PAGE FORMS ***

# *** patient page ***

#patient change password
@app.route('/patientChangePassword', methods=['GET', 'POST'])
def patientChangePassword():
    if request.method == 'POST':
        oldpassw = request.form['oldpassw']
        passw = request.form['passw']
        cpassw = request.form['cpassw']
        if passw == cpassw:
            obj = Database()
            username = session['username']
            if obj.setPatientPassword(oldpassw, passw, username) == True:
                return render_template('patienthome.html', msg="passwordChangeSuccess")

            else:
                return render_template('patienthome.html', msg="passwordChangeFailed")
        else:
            return render_template('patienthome.html', msg="passwordNotMatched")


#*** doctor page ***
#doctor change password
@app.route('/doctorChangePassword',methods=['GET','POST'])
def doctorChangePassword():
    if request.method == 'POST':
        oldpassw = request.form['oldpassw']
        passw = request.form['passw']
        cpassw = request.form['cpassw']
        if passw == cpassw:
            obj = Database()
            username = session['username']
            if obj.setDoctorPassword(oldpassw, passw, username) == True:
                return render_template('doctorhome.html', msg="passwordChangeSuccess")
            else:
                return render_template('doctorhome.html', msg="passwordChangeFailed")
        else:
            return render_template('doctorhome.html', msg="passwordNotMatched")

  
# updatePatientInfo # updated by samiksha

@app.route('/UpdatePatientInfo',methods=['GET','POST'])
def UpdatePatientInfo ():
    if request.method=='POST':

        name = request.form['name']
        dob = request.form['dob']
        gender = request.form['gender']
        email = request.form['email']
        mobile = request.form['mobile']
        address = request.form['address']


        obj1 = Database()
        status = obj1.UpdatePtInfo(name, dob, gender, email, mobile, address, session['username'])
        if status== True :
            session['data'] = [session['data'][0],name,dob,gender,email,mobile,address]
            return render_template('patienthome.html', msg="updateSuccess")
        else:
            return render_template('patienthome.html', msg="updateFailed")


# Raghvendra 29/05/2021 16:00 hrs
@app.route('/UpdateDoctorInfo',methods=['GET','POST'])
def UpdateDoctorInfo ():
    if request.method=='POST':
        #def UpdateDrInfo(self, name, qualification, gender, major, dob, email, mob, address, username):

        name = request.form['name']
        qualification = request.form['qualification']
        gender = request.form['gender']
        major = request.form['major']
        dob = request.form['dob']
        email = request.form['email']
        mobile = request.form['mobile']
        address = request.form['address']
        username = session['username']

        obj1 = Database()
        status = obj1.UpdateDoctorInfo(name, qualification, gender, major, dob, email, mobile, address, username)
        if status== True :
            data = [session['data'][0],name,qualification,gender,major,dob,email,mobile,address]
            session['data'] = data

            return render_template('doctorhome.html', msg="updateSuccess")
        else:
            return render_template('doctorhome.html', msg="updateFailed")


        

if __name__ == '__main__':
    app.run(debug=True)
