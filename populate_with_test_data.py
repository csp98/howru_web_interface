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
                        text=f'This is test question number {random.randint(1, 1e4)}',
                        creator=doctor,
                        language=random.choice(["ES", "GB"]),
                        public=True)
    question.save()
    doctor.assigned_questions.add(question)
    # Patients
    patient = Patient(identifier=random.randint(1, 1e4),
                      name=f'Patient number {random.randint(1, 1e4)}',
                      _gender=random.choice(["M", "F", "O"]),
                      username=f'username{random.randint(1, 1e4)}',
                      language=random.choice(["ES", "GB"])
                      )
    patient.schedule = "15:00"
    patient.picture = random.choice(AVATARS_LIST)
    patient.save()
    doctor.patient_set.add(patient)
    # Journal entries for each patient
    for j in range(random.randint(1,15)):
        # Pending questions
        pending = PendingQuestion(doctor=doctor,
                                  question=question,
                                  patient=patient,
                                  answering=False)
        pending.save()
        # Answered questions
        answered = AnsweredQuestion(doctor=doctor,
                                    question=question,
                                    patient=patient,
                                    answer_date=datetime.now(pytz.timezone('Europe/Madrid')).replace(
                                        hour=random.randint(0, 23), minute=random.randint(0,59)),
                                    response=f'response {j}')
        answered.save()
doctor.save()
print("Finished")
