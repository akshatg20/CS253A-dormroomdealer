# drd
This repository is the implementation of the course project CS253.
# Requirements
```python
pip install django
pip install Pillow
```
# Installation
```bash
git clone git@github.com:CS253-The-Dorm-Room-Dealer/dormroomdealer.git # ssh
cd dormroomdealer/project/
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```
# Guides for running the application

In settings.py you will find at line 136-137

```bash
EMAIL_HOST_USER = 'dummy-email-id'                          # put up your own email id here
EMAIL_HOST_PASSWORD = "dummy-email-app-password"            # put up your own app-generated password
```
The same email id also needs to be substituted at the following places:

In accounts/views.py ---> At lines 70, 159, 172, 328 and 342.

In items/views.py ----> At line 81.
