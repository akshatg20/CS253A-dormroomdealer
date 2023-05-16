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

# App-generated Password

1. Go to your Google Account.
2. Select Security
3. Under "Signing in to Google," select 2-Step Verification.
4. At the bottom of the page, select App passwords.
5. Enter a name that helps you remember where you’ll use the app password.
6. Select Generate.
7. To enter the app password, follow the instructions on your screen. The app password is the 16-character code that generates on your device.
8. Select Done.
