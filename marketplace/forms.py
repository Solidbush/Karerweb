from django import forms

from core.models import Karer

from .models import Product


class StateProductDashboardForm(forms.Form):

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.fields['product_id'] = forms.MultipleChoiceField(
            choices=Product.objects.filter(karer=self.request.user.karer).values_list('id', 'name'),
            label='Продукт'
        )
        if self.request.user.is_superuser:
            self.fields['karer_id'] = forms.MultipleChoiceField(
                choices=Karer.objects.values_list('id', 'name'),
                label='Обьект', required=False
            )
