from django.db.models import Count
from django.db.models.functions import Trunc

from core.charts.line_chart import LineChartDashboard

from .forms import ClientInviteDashboardForm, OrgInviteDashboardForm
from .models import ClientInvite, OrgInvite


class OrgInviteLineChart(LineChartDashboard):
    settings_form = OrgInviteDashboardForm
    title = 'Линейный график заявки юр. лицо'

    def init_with_context(self, context):
        if self.params:
            filter_params = {}
            if self.params.get('car'):
                filter_params['car_id__in'] = self.params.get('car')
            if self.params.get('driver'):
                filter_params['driver_id__in'] = self.params.get('driver')
            if self.params.get('karer'):
                filter_params['order__karer_id__in'] = self.params.get('karer')
            if self.params.get('organization'):
                filter_params['order__organization_id__in'] = self.params.get('organization')

            data = OrgInvite.objects.filter(**filter_params).annotate(
                _date=Trunc('create_at', self.params.get('period'))
            ).values('_date').annotate(
                _value=Count('id')
            ).values_list('_date', '_value').order_by('_date')

            for d in data:
                self.children.append((*d, 1))


class ClientInviteLineChart(LineChartDashboard):
    settings_form = ClientInviteDashboardForm
    title = 'Линейный график заявки физ. лицо'

    def init_with_context(self, context):
        if self.params:
            filter_params = {}
            if self.params.get('car'):
                filter_params['car_id__in'] = self.params.get('car')
            if self.params.get('driver'):
                filter_params['driver_id__in'] = self.params.get('driver')
            if self.params.get('karer'):
                filter_params['order__karer_id__in'] = self.params.get('karer')
            if self.params.get('client'):
                filter_params['order__client_id__in'] = self.params.get('client')

            data = ClientInvite.objects.filter(**filter_params).annotate(
                _date=Trunc('create_at', self.params.get('period'))
            ).values('_date').annotate(
                _value=Count('id')
            ).values_list('_date', '_value').order_by('_date')

            for d in data:
                self.children.append((*d, 1))
