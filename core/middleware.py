from django import forms
from django.utils.deprecation import MiddlewareMixin


class FormRequestMiddleware(MiddlewareMixin):
    def process_request(self, request):
        forms.BaseForm.request = request

    def process_response(self, request, response):
        if hasattr(forms.BaseForm, 'request'):
            del forms.BaseForm.request
        return response
