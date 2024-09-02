"""
# @Project sphinxcontrib-analytics
# @File    const.py
# @Author  MT308
# @Date    2024/9/2 1:05
"""
GOOGLE_GTAG = """
<!-- Google tag (gtag.js) -->
<script async src="https://www.googletagmanager.com/gtag/js?id=%s"></script>
"""

GOOGLE_SCRIPT = """
<script>
    window.dataLayer = window.dataLayer || [];
    function gtag(){dataLayer.push(arguments);}
    gtag('js', new Date());
    gtag('config', '%s');
</script>
"""

BAIDU_SCRIPT = """
<script>
var _hmt = _hmt || [];
(function() {
  var hm = document.createElement("script");
  hm.src = "https://hm.baidu.com/hm.js?%s";
  var s = document.getElementsByTagName("script")[0]; 
  s.parentNode.insertBefore(hm, s);
})();
</script>
"""
