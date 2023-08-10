from jet.dashboard.modules import DashboardModule


class LineChartDashboard(DashboardModule):
    template = "core/charts/line_chart.html"
    params = {}

    class Media:
        js = ('jet.dashboard/vendor/chart.js/Chart.min.js', 'core/charts/line_chart.js')

    def settings_dict(self):
        return self.params

    def load_settings(self, settings):
        self.params = settings

    def init_with_context(self, context):
        """self.children must be list of (x, y, t)"""
        return super().init_with_context(context)
