from jet.dashboard.modules import DashboardModule


class InfoDashboard(DashboardModule):
    template = "core/charts/info.html"
    params = {}

    def settings_dict(self):
        return self.params

    def load_settings(self, settings):
        self.params = settings

    def init_with_context(self, context):
        """self.children must be list of (x, y, t)"""
        return super().init_with_context(context)
