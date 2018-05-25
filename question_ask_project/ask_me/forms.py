from django import forms
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate

from ask_me.models import User, Question, Answer


text_validator = RegexValidator(r"[а-яА-Яa-zA-Z]",
                               "Text should contain letters")

tags_validator = RegexValidator(r"[а-яА-Яa-zA-Z]",
                               "Tags should contain letters")

password_validator = RegexValidator(r"^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$",
                                   "Password should contain minimum 8 characters, at least 1 letter and 1 number")



class UserRegistrationForm(forms.ModelForm):
    first_name = forms.CharField(validators=[text_validator], widget=forms.TextInput(attrs={
        'class': 'form-control',
        'minlength': 2,
        'maxlength': 30,
        'placeholder': 'First name'
    }))

    last_name = forms.CharField(validators=[text_validator],widget=forms.TextInput(attrs={
        'class': 'form-control',
        'minlength': 2,
        'maxlength': 30,
        'placeholder': 'Last name'
    }))

    username = forms.CharField(validators=[text_validator],widget=forms.TextInput(attrs={
        'class': 'form-control',
        'minlength': 5,
        'maxlength': 30,
        'placeholder': 'Username'}))

    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'class': 'form-control',
        'placeholder': 'E-mail'}))

    password = forms.CharField(validators=[password_validator], widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Password'}))

    password_confirmation = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Password confirmation'}))

    def clean(self):
        cleaned_data = super(UserRegistrationForm, self).clean()
        password = cleaned_data.get("password")
        password_confirmation = cleaned_data.get("password_confirmation")

        if password != password_confirmation:
            raise ValidationError("Password and Confirm password does not match")
        return cleaned_data

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'upload']



class UserLoginForm(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'maxlength': 30,
        'placeholder': 'Username'}))

    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Password'}))

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        if not user or not user.is_active:
            raise ValidationError("Sorry, that login or password is invalid. Please try again.")
        return self.cleaned_data

    class Meta:
        model = User
        fields = ['username', 'password']



class UserSettingsForm(forms.ModelForm):
    first_name = forms.CharField(required=False,validators=[text_validator],widget=forms.TextInput(attrs={
        'class': 'form-control',
        'minlength': 2,
        'maxlength': 30,
        'placeholder': 'First name'}))

    last_name = forms.CharField(required=False,validators=[text_validator], widget=forms.TextInput(attrs={
        'class': 'form-control',
        'minlength': 2,
        'maxlength': 30,
        'placeholder': 'Last name'}))

    username = forms.CharField(validators=[text_validator],required=False,widget=forms.TextInput(attrs={
        'class': 'form-control',
        'minlength': 5,
        'maxlength': 30,
        'placeholder': 'Username'}))

    email = forms.EmailField(required=False,widget=forms.EmailInput(attrs={
        'class': 'form-control',
        'placeholder': 'E-mail'}))

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'upload']



class NewQuestionForm(forms.ModelForm):
    title = forms.CharField(validators=[text_validator],widget=forms.TextInput(attrs={
        'class': 'form-control',
        'maxlength': 100,
        'minlength': 5,
        'placeholder': 'Title'}))

    text = forms.CharField(validators=[text_validator],widget=forms.Textarea(attrs={
        'class': 'form-control',
        'minlength': 5,
        'placeholder': 'Write your question here...'}))

    tags = forms.CharField(required=False, validators=[text_validator],widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'List here tags by separating them with a space.'}))

    def clean(self):
        title = self.cleaned_data.get('title')
        tags = self.cleaned_data.get('tags')
        if len(str(title)) > 100:
            raise ValidationError("Sorry, a title should contain no more than 100 characters. ")
        if len(str(tags)) > 20:
            raise ValidationError("Sorry, length of tags line must be no more than 20 characters.  ")
        return self.cleaned_data

    class Meta:
        model = Question
        fields = ['title', 'text', 'tags']



class AnswerForm(forms.ModelForm):
    text = forms.CharField(widget=forms.Textarea(attrs={
        'class': 'form-control',
        'minlength': 1,
        'placeholder': 'Write your answer here...'}))

    class Meta:
        model = Answer
        fields = ['text']