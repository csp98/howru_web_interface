import os
from datetime import datetime

import pytz

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")
from howru_models.models import *
from django.contrib.auth.models import User

# Get doctor
doctor = User.objects.get(username='carlossanchez').doctor
# Create question
for i in range(200):
    # Questions
    question = Question(responses=["response 1", "response 2", "response 3", "response 4"],
                        text=f'This is test question number {i}',
                        creator_id=doctor,
                        language="GB",
                        public=True)
    question.save()
    doctor.assigned_questions.add(question)
    doctor.save()
    # Patients
    patient = Patient(identifier=i,
                      name=f'Patient number {i}',
                      _gender="M",
                      username=f'username{i}',
                      language="ES",
                      assigned_doctor=doctor
                      )
    patient.schedule="15:00"
    patient.picture = '/opt/web_interface/core/static/assets/favicon/icon.png'
    patient.save()
    # Pending questions
    pending = PendingQuestion(doctor_id=doctor,
                              question_id=question,
                              patient_id=patient,
                              answering=False)
    pending.save()
    # Answered questions
    answered = AnsweredQuestion(doctor_id=doctor,
                                question_id=question,
                                patient_id=patient,
                                answer_date=datetime.now(pytz.timezone('Europe/Madrid')),
                                response=f'response {i}')
    answered.save()
print("Finished")
