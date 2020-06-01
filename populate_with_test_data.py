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
questions = list()
patients = list()
# Create question
for i in range(20):
    # Questions
    question = Question(responses=["response 1", "response 2", "response 3", "response 4"],
                        text=f'This is test question number {i}',
                        creator=doctor,
                        language=random.choice(["ES", "GB"]),
                        public=True,
                        assigned_to_all=True)
    question.save()
    questions.append(question)
    doctor.assigned_questions.add(question)
    # Patients
    patient = Patient(identifier=i,
                      name=f'Patient number {i}',
                      _gender=random.choice(["M", "F", "O"]),
                      username=f'username{i}',
                      language=random.choice(["ES", "GB"])
                      )
    patient.schedule = "15:00"
    patient.picture = random.choice(AVATARS_LIST)
    patient.save()
    patients.append(patient)
    doctor.patient_set.add(patient)
    doctor.save()

# Journal entries for each patient
for patient in patients:
    for question in questions:
        # Pending questions
        pending = PendingQuestion(doctor=doctor,
                                  question=question,
                                  patient=patient,
                                  answering=False)
        pending.save()
        for j in range(1, 28):
            # Answered questions
            answered = AnsweredQuestion(doctor=doctor,
                                        question=question,
                                        patient=patient,
                                        answer_date=datetime.now(pytz.timezone('Europe/Madrid')).replace(
                                            hour=random.randint(0, 23), minute=random.randint(0, 59),
                                            day=j, month=random.randint(1,12)),
                                        response=random.choice(
                                            ["response 1", "response 2", "response 3", "response 4"]))
            answered.save()
print("Finished")
