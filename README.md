# 🚀 Telerehabilitation App
 
Telemedicine is a way to access healthcare appointments with healthcare providers on the internet using your phone or computer. These appointments are usually video calls with online chat messaging through an app or platform. It is not meant to replace clinic visits with a doctor but instead should complement regular healthcare. The objective of this project is to use telemedicine patients to access physical therapy services.
 
## 👤 System Admin
- [x] Can approve/deny requests for creation of physical therapist account
- [x] Can approve/deny requests for creation of patient account
- [x] Can enable/disable physical therapist or patient account

## 👤 Physical Therapist
- [x] Request for creation of physical therapist account
- [x] Login
- [x] Forgot password
- [ ] View dashboard
	- [x] Profile Tab
		- [x] View profile
		- [x] Update profile
		- [ ] Create clinic hours (input time, day Ex. MWF 9am-12noon; 1pm-4pm
		- [ ] Update clinic hours
		- [ ] Create teleconsultation hours
		- [ ] Update teleconsultationhours

	- [ ] Patients Tab
		- [ ] View active patients (i.e. patients with scheduled current or future clinic/teleconsultation appointment)
		- [ ] View inactive patients (i.e. patients who had previous appointments or teleconsultations but no current or future appointments/teleconsultations)
		- [ ] View specific patient
			- [ ] View doctor's orders
			- [ ] View patient general clinical and physio-clinical history, treatment plan and treatment notes, lab results, other pictures/videos

		Note: If the patient was patient of another physical therapist in the past, the current physical therapist should still be able to view his past records with  the physical therapist. (i.e. view - [ ] C. iii-iv.)

	- [ ] Appointments Tab (Monthly Calendar Format)
		- [ ] View calendar of scheduled clinic or teleconsultation appointments
		- [ ] View a specific clinic/teleconsultation appointment
		- [ ] Send clinic/teleconsultation appointment reminders to patients
		- [ ] View patient requests for clinic/teleconsultation appointments
		- [ ] Approve, suggest an alternative schedule, or deny a patient request for clinic/teleconsultation appointment
		- [ ] Update patient Record
			- [ ] Input patient general clinical history
			- [ ] Input patient  physio clinical history
			- [ ] Input patient treatment plan and treatment notes
			- [ ] View patient uploaded laboratory results, pictures, video

	- [ ] Teleconferencing Tab
		- [ ] Select patients with approved teleconferencing appointment scheduled now
		- [ ] Perform teleconsultation (live video)
		- [ ] Update patient Record
			- [ ] Input patient general clinical history
			- [ ] Input patient  physio clinical history
			- [ ] Input patient treatment plan and treatment notes
			- [ ] View patient uploaded laboratory results, pictures, video

	- [ ] Exercise Videos Tab
		- [ ] YouTube link of exercise videos (unlisted)
 
 
## 👤 Patient
- [x] Request for patient account
- [x] Login
- [x] Forgot Password
- [ ] Search Tab
	- [x] View list of physical therapists
	- [x] View profile of a specific physical therapist
		i. View clinic and teleconsultation hours tab of a specific physical therapist
- [ ] Appointments Tab
	- [x] Request for clinical (physical) appointment
	- [x] Request for teleconsultation appointment
	- [x] View status of requested clinical (physical) appointment
	- [x] View status of requested teleconsultation appointment

- [ ] Patient's Record Tab
	- [ ] View personal info
	- [ ] Update personal info
	- [ ] Upload doctor's orders
	- [ ] Upload laboratory results (pdf)
	- [ ] Upload pictures of injury (jpg)
	- [ ] Upload video (mp4)

- [ ] Messages Tab
	- [x] View reminders of clinical/teleconsultation appointments
	- [x] Messages to/from physical therapist (ex. YouTube links to exercise videos)
 

## Heroku Postgres Database Credentials
- Host
	ec2-52-73-155-171.compute-1.amazonaws.com
- Database
    d6hlvm3t5csmko
- User
    inbsnfpxmpenfc
- Port
    5432
- Password
    bb68d64d00fc0ad543a07a3e104808094a9e681150d93a1b349bb575ae5063d0
- URI
    postgres://inbsnfpxmpenfc:bb68d64d00fc0ad543a07a3e104808094a9e681150d93a1b349bb575ae5063d0@ec2-52-73-155-171.compute-1.amazonaws.com:5432/d6hlvm3t5csmko
- Heroku CLI
    heroku pg:psql postgresql-fluffy-69157 --app kmontrainingpy

## Django Admin Superuser account
create own. use local db. 
