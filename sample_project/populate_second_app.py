import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "sample_project.settings")

import django
django.setup()

##FAKE POP SCRIPT
import random
from sample_app.models import AccessRecord, Topic, Webpage, User
from faker import Faker

fakegen = Faker()
topics = ['Search', "Social", "Marketplace", "News", "Games"]

def add_topic():
    t = Topic.objects.get_or_create(top_name=random.choice(topics))[0]
    t.save()
    return t

def populate(N=5):

    for entry in range(N):
        #get the Topic for the entry
        top = add_topic()

        #create fake data for the entry
        fake_url = fakegen.url()
        fake_date = fakegen.date()
        fake_name = fakegen.company()

        #create the new webpage entry
        webp = Webpage.objects.get_or_create(topic=top, url=fake_url, name=fake_name)[0]

        #create the access record for the Webpage
        acc_rec = AccessRecord.objects.get_or_create(name=webp, date=fake_date)[0]

def populate_users(N=5):

    for entry in range(N):
        fake_fname = fakegen.first_name()
        fake_lname = fakegen.last_name()
        fake_email = fakegen.email()
        fake_dob = fakegen.date()
        fake_notes = fakegen.paragraph()

        user = User.objects.get_or_create(first_name=fake_fname,
                                            last_name=fake_lname,
                                            email=fake_email,
                                            DoB=fake_dob,
                                            notes=fake_notes
                                            )[0]

if __name__ == '__main__':
    print ("populating script!")
    populate(20)
    populate_users(20)
    print ("populating complete")
