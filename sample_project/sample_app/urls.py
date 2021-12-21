from django.conf.urls import url
from sample_app import views
from django.urls import path

#TEMPLATE TAGGING - allowing the use of e.g. relative url in templates
app_name = 'sample_app'

urlpatterns = [
    #Example in HTML: <a href="{% url 'sample_app:relative' %}
    # 'sample_app' refers to the app_name
    # 'relative refers' to the name attribute below
    #This allows dev to avoid including actual paths in HTML.
    path('relative/', views.relative_url_templates, name='relative'),
    path('help/', views.help, name="help"),
    path('users/', views.user, name="users"),
    path('formpage/', views.form_name_view, name='form_name'),
    path('userformpage/', views.form_user_enter, name='form_enter_user'),
    # path('base_temp/', views.base_template, name='base_template')
    path('register/', views.register, name='register'),
    path('user_login/', views.user_login, name='user_login')
]
