from flask_login import login_required


class LoginRequiredMixin:

    @login_required
    def dispatch_request(self, *args, **kwargs):
        return super().dispatch_request(*args, **kwargs)
