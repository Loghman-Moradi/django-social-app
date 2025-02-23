from django import forms
from .models import *
from django.contrib.auth.forms import AuthenticationForm


class LoginForm(AuthenticationForm):
    username = forms.CharField(max_length=250, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(max_length=250, required=True, widget=forms.PasswordInput(attrs={'class': "form-control"}))


class UserRegisterForm(forms.ModelForm):
    password = forms.CharField(max_length=20, required=True, label="رمز عبور",
                               widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    repeat_password = forms.CharField(max_length=20, required=True, label="تکرار رمز عبور",
                                      widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'phone']

    def clean_repeat_password(self):
        cd = self.cleaned_data
        if cd['password'] != cd['repeat_password']:
            raise forms.ValidationError('رمز عبور و تکرار آن مطابقت ندارد')
        return cd['repeat_password']

    def clean_phone(self):
        phone = self.cleaned_data['phone']
        if User.objects.filter(phone=phone).exists():
            raise forms.ValidationError('phone already exists!')
        return phone


class EditUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'date_of_birth', 'email', 'phone', 'job', 'bio', 'photo']

    def clean_phone(self):
        phone = self.cleaned_data['phone']
        if User.objects.exclude(id=self.instance.id).filter(phone=phone).exists():
            raise forms.ValidationError('phone already exists!')
        return phone

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.exclude(id=self.instance.id).filter(username=username).exists():
            raise forms.ValidationError('username already exists!')
        return username


class TicketForm(forms.ModelForm):
    SUBJECT_CHOICE = (
        ("پیشنهاد", "پیشنهاد"),
        ("انتقاد", "انتقاد"),
        ("گزارش", "گزارش"),
    )
    subject = forms.ChoiceField(choices=SUBJECT_CHOICE, label="موضوع")

    class Meta:
        model = Ticket
        fields = ['fullname', 'email', 'phone_number', 'message', 'subject']


class PostForm(forms.ModelForm):
    image_1 = forms.ImageField(label="تصوبر اول")
    image_2 = forms.ImageField(label="تصوبر دوم")

    class Meta:
        model = Post
        fields = ['description', 'tags']


class SearchForm(forms.Form):
    query = forms.CharField()












