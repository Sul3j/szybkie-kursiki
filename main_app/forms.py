from django import forms
from .models import Course

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = '__all__'

    def clean_icon(self):
        icon = self.cleaned_data.get('icon')
        if not icon.startswith(('fas ', 'fab ', 'far ', 'fal ', 'fad ', 'fa-solid', 'fa-light', 'fa-regular', 'fa-brands ')):
            raise forms.ValidationError(
                "Ikona musi zaczynać się od jednego z prefixów: fas, fab, far, fal, fad, fa-brands"
            )
        return icon