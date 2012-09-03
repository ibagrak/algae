import os
import jinja2
from webapp2_extras import i18n

jinja_environment = jinja2.Environment(loader=jinja2.FileSystemLoader('static/templates'),extensions=['jinja2.ext.i18n'])
jinja_environment.install_gettext_callables(
  i18n.gettext,
  i18n.ngettext,
  newstyle=True)
jinja_environment.filters.update({
  'format_date'     : i18n.format_date,
  'format_time'     : i18n.format_time,
  'format_datetime' : i18n.format_datetime,
  'format_timedelta': i18n.format_timedelta
})
