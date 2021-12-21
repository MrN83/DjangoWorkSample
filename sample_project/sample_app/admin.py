from django.contrib import admin
from sample_app.models import AccessRecord, Topic, Webpage, WebUser, UserProfileInfo

# Register your models here. -> don't foget to create a superuser as well!
# Superuser: name="tue" pass="pass123", email: "duckrates@gmail.com"
admin.site.register(AccessRecord)
admin.site.register(Topic)
admin.site.register(Webpage)
admin.site.register(WebUser)
admin.site.register(UserProfileInfo)
