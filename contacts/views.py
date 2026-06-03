from django import forms
from django.contrib import messages
from django.shortcuts import redirect, render
from django.urls import reverse

from .models import ContactMessage
from core.seo import breadcrumb_schema, local_business_schema, seo_context


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
    site_setting = getattr(request, 'site_setting', None)
    return render(request, 'contact.html', {
        'form': form,
        **seo_context(
            request,
            title=f'Lien he bao gia phu tung o to | {getattr(site_setting, "site_name", "") or "AutoParts"}',
            description='Lien he tu van, bao gia phu tung o to chinh hang va ho tro tim dung ma san pham.',
            canonical_path=reverse('contacts:contact'),
            json_ld=[
                local_business_schema(request, site_setting),
                breadcrumb_schema(request, [('Trang chủ', reverse('core:home')), ('Liên hệ', reverse('contacts:contact'))]),
            ],
        ),
    })

# Create your views here.
