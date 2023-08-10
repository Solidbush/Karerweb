from collections import defaultdict

from core.charts.line_chart import LineChartDashboard
from invite.models import ClientInvite, OrgInvite

from .forms import InviteDashboardForm


class InviteLineChart(LineChartDashboard):
    settings_form = InviteDashboardForm
    title = 'Линейный график заявки'

    def init_with_context(self, context):
        if self.params:
            dataset = defaultdict(list)
            data = OrgInvite.objects.values_list('create_at__date', 'id')
            for d in data:
                dataset[d[0]].append(d[1])
            data = ClientInvite.objects.values_list('create_at__date', 'id')
            for d in data:
                dataset[d[0]].append(d[1])
            for date, v in dataset.items():
                self.children.append((date, len(v), 1))
