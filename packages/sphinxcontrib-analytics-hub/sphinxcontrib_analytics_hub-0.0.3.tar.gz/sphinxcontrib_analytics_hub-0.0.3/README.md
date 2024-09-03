# Sphinxcontrib-Analytics-Hub

## About

Sphinx extension for googleanalytics and baidu analytics .

Based on [sphinx-contrib/googleanalytics](https://github.com/sphinx-contrib/googleanalytics) and add baidu analytics .

## Install

with `pip`:

```commandline
pip install sphinxcontrib-analytics-hub
```

## Using

Just add `sphinxcontrib_analytics_hub` to the list of extension in the `conf.py` file .

For example:

```python
extensions = [
    ...,
    'sphinxcontrib_analytics_hub',
]
```

### Config items:

|    config name    |        value        | value type | default |                     description                     |
|:-----------------:|:-------------------:|:----------:|:-------:|:---------------------------------------------------:|
| analytics_enabled |  `True` or `False`  |    bool    | `True`  | set `True` to enable analytics, `False` to ruff off |
|  analytics_with   | `google` or `baidu` |    str     |  `''`   |                   analytics name                    |
|   analytics_id    |    analytics id     |    str     |   ``    |          the analytics id google or baidu           |

For example of analytics with [google](https://analytics.google.com/analytics/web/provision/#/provision) :

```python
# conf.py

...

analytics_with = 'google'
analytics_id = 'xxxxxxxxxxxxx'
```

For example of analytics with baidu :

```python
# conf.py

...

analytics_with = 'baidu'
analytics_id = 'xxxxxxxxxxxxx'
```

## Supported platforms

Now:
- [google](https://analytics.google.com/analytics/web/provision/#/provision)
- [baidu](https://tongji.baidu.com/)


More analytics platforms will be added in the future.