from flask import Blueprint, request, redirect, render_template, url_for
from flask.views import MethodView

pages = Blueprint('pages', __name__, template_folder='templates')

class BaseView(MethodView):
  def get(self):
    return render_template('base.html')
#Site is a single page
pages.add_url_rule('/',view_func=BaseView.as_view('pages'))