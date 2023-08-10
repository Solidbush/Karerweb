from core.mixins import ManualModeMixin, RecoverModeMixin

from .models import invite_schedules


class RecoverInviteModeMixin(RecoverModeMixin):
    def perform_invite_recover(self, invite):
        super(RecoverInviteModeMixin, self).perform_invite_recover(invite)
        invite_schedules(self.recover_model, invite, True)


class ManualInviteModeMixin(ManualModeMixin):
    def perform_invite_manual(self, invite):
        print(invite)
