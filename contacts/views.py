from django import forms
from django.contrib import messages
from django.shortcuts import redirect, render

from .models import ContactMessage


class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['full_name', 'phone', 'email', 'message']
        widgets = {
            'full_name': forms.TextInput(attrs={'placeholder': 'Họ tên'}),
            'phone': forms.TextInput(attrs={'placeholder': 'Số điện thoại'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Email'}),
            'message': forms.Textarea(attrs={'placeholder': 'Nội dung cần tư vấn', 'rows': 5}),
        }


def contact(request):
    form = ContactForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Cảm ơn bạn đã liên hệ. Chúng tôi sẽ phản hồi sớm.')
        return redirect('contacts:contact')
    return render(request, 'contact.html', {'form': form})

# Create your views here.
