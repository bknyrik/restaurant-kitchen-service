from flask import render_template


def page_not_found_404(error: str) -> tuple[str, int]:
    return render_template("404.html"), 404


def forbidden_403(error: str) -> tuple[str, int]:
    return render_template("403.html"), 403
