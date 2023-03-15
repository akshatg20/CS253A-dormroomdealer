# from django import forms
# from django.core.exceptions import ValidationError

# class DateRangeField(forms.Field):
#     def validate(self, value):
#         start_date = value.get('start_date')
#         end_date = value.get('end_date')
#         if end_date and start_date:
#             if end_date < start_date:
#                 raise ValidationError("End date should be greater than start date")

# class DateRangeForm(forms.Form):
#     start_date = forms.DateField()
#     end_date = forms.DateField()
#     date_range = DateRangeField()
