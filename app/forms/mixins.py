from wtforms import StringField


class SearchByNameMixin:
    name = StringField(
        render_kw={
            "class": "form-control",
            "placeholder": "Search by name"
        }
    )
