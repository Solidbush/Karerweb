from jet.dashboard import modules
from jet.dashboard.dashboard import AppIndexDashboard as _AppIndexDashboard
from jet.dashboard.dashboard import Dashboard

from core.dashboard import InviteLineChart
from import_invite.dashboard import OrgImportInviteLineChart
from invite.dashboard import ClientInviteLineChart, OrgInviteLineChart
from marketplace.dashboard import StateProductDashboard


class AppIndexDashboard(_AppIndexDashboard):

    def init_with_context(self, context):
        self.available_children.append(modules.ModelList)
        self.available_children.append(modules.RecentActions)
        if self.app_label not in ['marketplace']:
            self.available_children.append(OrgInviteLineChart)
            self.available_children.append(ClientInviteLineChart)
            self.available_children.append(OrgImportInviteLineChart)
        if self.app_label == 'marketplace':
            self.available_children.append(StateProductDashboard)


class IndexDashboard(Dashboard):
    columns = 1

    def init_with_context(self, context):
        self.available_children.append(modules.AppList)
        self.available_children.append(modules.RecentActions)
        self.available_children.append(InviteLineChart)
