"""
# @Project sphinxcontrib-analytics
# @File    analytics.py
# @Author  MT308
# @Date    2024/9/1 23:44
"""
from sphinx.application import Sphinx
from sphinx.util import logging
from sphinx.errors import ExtensionError

from sphinxcontrib_analytics_hub.const import GOOGLE_GTAG, GOOGLE_SCRIPT, BAIDU_SCRIPT

ANALYTICS_WITH = ["google", "baidu"]

_logger = logging.getLogger(__name__)


def add_analytics_javascript(app: Sphinx, pagename, templatename, context, doctree):
    if not app.config.analytics_enabled:
        _logger.info("Skipping analytics javascript generation at %s" % pagename)
        return
    metatags = context.get('metatags', '')
    if app.config.analytics_with == 'google':
        metatags += GOOGLE_GTAG % app.config.analytics_id
        metatags += GOOGLE_SCRIPT % app.config.analytics_id
    else:
        metatags += BAIDU_SCRIPT % app.config.analytics_id

    context['metatags'] = metatags


def check_config(app: Sphinx):
    if not app.config.analytics_id:
        raise ExtensionError(
            "'analytics_id' config value must be set for google or baidu statistics to function properly.")
    if not app.config.analytics_with in ANALYTICS_WITH:
        raise ExtensionError(
            "'analytics_id' config value must be one of 'google' or 'baidu'")
