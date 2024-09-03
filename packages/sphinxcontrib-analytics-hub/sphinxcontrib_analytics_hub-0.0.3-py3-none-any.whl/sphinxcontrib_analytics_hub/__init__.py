from sphinx.application import Sphinx
from sphinx.util.typing import ExtensionMetadata

from sphinxcontrib_analytics_hub import __version__
from sphinxcontrib_analytics_hub.analytics import add_analytics_javascript, check_config


def setup(app: Sphinx) -> ExtensionMetadata:
    # config for analytics
    app.add_config_value('analytics_enabled', True, 'html')
    app.add_config_value('analytics_with', 'google', 'html')
    app.add_config_value('analytics_id', '', 'html')

    # hooks for analytics
    app.connect('builder-inited', check_config)
    app.connect('html-page-context', add_analytics_javascript)

    return {
        'parallel_read_safe': True,
        'parallel_write_safe': True,
        'version': __version__,
    }