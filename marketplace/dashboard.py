from django.db.models import Q, Sum

from core.charts.info import InfoDashboard
from import_invite.models import OrgImportInvite
from invite.models import ClientInvite, OrgInvite
from marketplace.models import Product

from .forms import StateProductDashboardForm


class StateProductDashboard(InfoDashboard):
    title = "Состаяние продукта"
    settings_form = StateProductDashboardForm

    def load_settings(self, settings):
        super().load_settings(settings)
        self.title = f"""{self.title} - {', '.join(
            Product.objects.filter(id__in=self.params.get('product_id', [])).values_list('name', flat=True)
        )}"""

    def init_with_context(self, context):
        if self.params:
            request = context['request']
            if request.user.is_superuser:
                if self.params.get('karer_id'):
                    imports = OrgImportInvite.objects.filter(
                        product_id__in=self.params['product_id'], order__karer_id__in=self.params['karer_id']
                    ).aggregate(sum=Sum('weight'))['sum'] or 0
                    exports = OrgInvite.objects.filter(
                        ~Q(status__in=["canceled"]), product_id__in=self.params['product_id'],
                        order__karer_id__in=self.params['karer_id']
                    ).aggregate(sum=Sum('weight'))['sum'] or 0 + \
                        (ClientInvite.objects.filter(
                            ~Q(status__in=["canceled"]), product_id__in=self.params['product_id'],
                            order__karer_id__in=self.params['karer_id']
                        ).aggregate(sum=Sum('weight'))['sum'] or 0)
                else:
                    imports = OrgImportInvite.objects.filter(
                        product_id__in=self.params['product_id']
                    ).aggregate(sum=Sum('weight'))['sum'] or 0
                    exports = OrgInvite.objects.filter(
                        ~Q(status__in=["canceled"]), product_id__in=self.params['product_id']
                    ).aggregate(sum=Sum('weight'))['sum'] or 0 + \
                        (ClientInvite.objects.filter(
                            ~Q(status__in=["canceled"]), product_id__in=self.params['product_id']
                        ).aggregate(sum=Sum('weight'))['sum'] or 0)
            else:
                imports = OrgImportInvite.objects.filter(
                    product_id__in=self.params['product_id'], order__karer_id__in=[request.user.karer_id]
                ).aggregate(sum=Sum('weight'))['sum'] or 0
                exports = OrgInvite.objects.filter(
                    product_id__in=self.params['product_id'], order__karer_id__in=[request.user.karer_id]
                ).aggregate(sum=Sum('weight'))['sum'] or 0 + \
                    (ClientInvite.objects.filter(
                        product_id__in=self.params['product_id'], order__karer_id__in=[request.user.karer_id]
                    ).aggregate(sum=Sum('weight'))['sum'] or 0)
            delta = imports - exports
            self.children.append({'title': "Импорты", 'value': imports})
            self.children.append({'title': "Экспорты", 'value': exports})
            self.children.append({'title': "Остаток", 'value': delta})
