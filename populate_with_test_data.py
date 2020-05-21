import os
import random
from datetime import datetime

import pytz

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")
from howru_models.models import *
from django.contrib.auth.models import User
AVATARS_PATH = '/opt/web_interface/core/static/assets/img/avatars'
AVATARS_LIST = [f'{AVATARS_PATH}/{image}' for image in os.listdir(AVATARS_PATH)]
# Get doctor
doctor = User.objects.get(username='data_populator').doctor
# Create question
for i in range(200):
    # Questions
    question = Question(responses=["response 1", "response 2", "response 3", "response 4"],
                        text=f'This is test question number {i}',
                        creator_id=doctor,
                        language=random.choice(["ES", "GB"]),
                        public=True)
    question.save()
    doctor.assigned_questions.add(question)
    # Patients
    patient = Patient(identifier=random.randint(1, 1e4),
                      name=f'Patient number {i}',
                      _gender=random.choice(["M", "F", "O"]),
                      username=f'username{i}',
                      language=random.choice(["ES", "GB"])
                      )
    patient.schedule = "15:00"
    patient.picture = random.choice(AVATARS_LIST)
    patient.save()
    doctor.patient_set.add(patient)

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
                                answer_date=datetime.now(pytz.timezone('Europe/Madrid')).replace(
                                    hour=random.randint(0, 23), minute=random.randint(0,59)),
                                response=f'response {i}')
    answered.save()
doctor.save()
print("Finished")
