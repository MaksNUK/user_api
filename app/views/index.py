from flask import url_for, redirect


def index(error):
    return redirect(
        url_for('/api/v1_0./api/v1_0_swagger_ui_index')
    )
