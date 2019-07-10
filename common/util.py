import yaml
import requests
import time
import io
from common.cls import SingleMode


class Config(metaclass=SingleMode):

    def __init__(self, path="config/config.yml"):

        self.conf = None
        self.path = path
        self._read()

    def _read(self):
        with open(self.path) as f:
            conf = yaml.safe_load(f)
            self.conf = conf


class Cookie(object):
    """
    通过splash获取cookie
    """
    def __init__(self, url="http://2.taobao.com"):
        self.cookie = ""
        self.conf = Config().conf
        self.req = requests.Session()
        self.SPLASH_URL = "http://{0}:{1}/run".format(self.conf["SPLASH"]["URL"], self.conf["SPLASH"]["PORT"])
        self.script = """
            splash:go(args.url)
            return splash:get_cookies()
            """
        self.token = None
        self.url = url
        self.get_cookie()

    def get_cookie(self):
        try:
            res = self.req.post(self.SPLASH_URL, json={'lua_source': self.script, 'url': self.url, 'wait': '5.0'},
                                timeout=10)
            for i in res.json():
                if i['name'] == "_m_h5_tk":
                    self.token = str(i['value']).split("_")[0]
                self.cookie += "{name}={value}; ".format(name=i['name'], value=i['value'])
        except Exception as e:
            print(e)
            exit(1)


class JServer(object):
    """
    上传js文件流到服务器,让服务器解释js脚本并返回结果
    """
    def __init__(self, payload="Date.now()"):
        self.conf = Config().conf
        self.jServer = "{0}:{1}".format(self.conf["JServer"]["URL"], self.conf["JServer"]["PORT"])
        self.req = requests.Session()
        self.payload = payload
        self.get(self.payload)

    def get(self, payload):
        try:

            r = self.req.post(url="http://%s/jsFile" % self.jServer,
                              # files={"file":("文件名","文件流")}
                              files={'file': (str(time.time()) + '.js', io.StringIO(payload))},
                              timeout=10
                              )
            return r.json()
        except Exception as e:
            print(e)
            return None


def generate_js(page_number, token):
    """
    该函数已确保生成的sign是正确的
    该js的链接:https://g.alicdn.com/idleFish-F2e/idle-pc/1.0.15/home/index-min.js:formatted(代码大致在41576行)
    用谷歌浏览器调试,即可知道结构
    :param page_number: 页码
    :param token:  cookie中_m_h5_tk的前半部分(_分割)
    :return:返回组合的生成的js字符串和当前的时间戳
    """
    timestamp = int(str(time.time())[:14].replace(".", ""))
    # timestamp = 1562656744827
    js = r"""n={api:"mtop.taobao.idle.home.tabfeeds",dataType:"jsonp",type: "get",v: "3.0",data:'\{"spmPrefix":"a2170.7897990.6801272.","trackName":"Feed1","needBanner":"true","abtag":"style_masonryLayouts_1.0_mamaAD","pageNumber":%s\}'};
    """ % page_number
    js += r"""i={token:"%s"};""" % token

    js += r"""a=%s;
    """ % timestamp
    js += r"""s="12574478";
    l = function(e) {
                function t(e, t) {
                    return e << t | e >>> 32 - t
                }
                function n(e, t) { 
                    var n, i, r, o, s;
                    return r = 2147483648 & e,
                    o = 2147483648 & t,
                    s = (1073741823 & e) + (1073741823 & t),
                    (n = 1073741824 & e) & (i = 1073741824 & t) ? 2147483648 ^ s ^ r ^ o : n | i ? 1073741824 & s ? 3221225472 ^ s ^ r ^ o : 1073741824 ^ s ^ r ^ o : s ^ r ^ o
                }
                function i(e, i, r, o, s, a, l) {
                    return n(t(e = n(e, n(n(function(e, t, n) {
                        return e & t | ~e & n
                    }(i, r, o), s), l)), a), i)
                }
                function r(e, i, r, o, s, a, l) {
                    return n(t(e = n(e, n(n(function(e, t, n) {
                        return e & n | t & ~n
                    }(i, r, o), s), l)), a), i)
                }
                function o(e, i, r, o, s, a, l) {
                    return n(t(e = n(e, n(n(function(e, t, n) {
                        return e ^ t ^ n
                    }(i, r, o), s), l)), a), i)
                }
                function s(e, i, r, o, s, a, l) {
                    return n(t(e = n(e, n(n(function(e, t, n) {
                        return t ^ (e | ~n)
                    }(i, r, o), s), l)), a), i)
                }
                function a(e) {
                    var t, n = "", i = "";
                    for (t = 0; 3 >= t; t++)
                        n += (i = "0" + (e >>> 8 * t & 255).toString(16)).substr(i.length - 2, 2);
                    return n
                }
                var l, u, c, d, f, h, p, m, v, g;
                for (g = function(e) {
                    for (var t, n = e.length, i = n + 8, r = 16 * ((i - i % 64) / 64 + 1), o = new Array(r - 1), s = 0, a = 0; n > a; )
                        s = a % 4 * 8,
                        o[t = (a - a % 4) / 4] = o[t] | e.charCodeAt(a) << s,
                        a++;
                    return s = a % 4 * 8,
                    o[t = (a - a % 4) / 4] = o[t] | 128 << s,
                    o[r - 2] = n << 3,
                    o[r - 1] = n >>> 29,
                    o
                }(e = function(e) {
                    e = e.replace(/\r\n/g, "\n");
                    for (var t = "", n = 0; n < e.length; n++) {
                        var i = e.charCodeAt(n);
                        128 > i ? t += String.fromCharCode(i) : i > 127 && 2048 > i ? (t += String.fromCharCode(i >> 6 | 192),
                        t += String.fromCharCode(63 & i | 128)) : (t += String.fromCharCode(i >> 12 | 224),
                        t += String.fromCharCode(i >> 6 & 63 | 128),
                        t += String.fromCharCode(63 & i | 128))
                    }
                    return t
                }(e)),
                h = 1732584193,
                p = 4023233417,
                m = 2562383102,
                v = 271733878,
                l = 0; l < g.length; l += 16)
                    u = h,
                    c = p,
                    d = m,
                    f = v,
                    p = s(p = s(p = s(p = s(p = o(p = o(p = o(p = o(p = r(p = r(p = r(p = r(p = i(p = i(p = i(p = i(p, m = i(m, v = i(v, h = i(h, p, m, v, g[l + 0], 7, 3614090360), p, m, g[l + 1], 12, 3905402710), h, p, g[l + 2], 17, 606105819), v, h, g[l + 3], 22, 3250441966), m = i(m, v = i(v, h = i(h, p, m, v, g[l + 4], 7, 4118548399), p, m, g[l + 5], 12, 1200080426), h, p, g[l + 6], 17, 2821735955), v, h, g[l + 7], 22, 4249261313), m = i(m, v = i(v, h = i(h, p, m, v, g[l + 8], 7, 1770035416), p, m, g[l + 9], 12, 2336552879), h, p, g[l + 10], 17, 4294925233), v, h, g[l + 11], 22, 2304563134), m = i(m, v = i(v, h = i(h, p, m, v, g[l + 12], 7, 1804603682), p, m, g[l + 13], 12, 4254626195), h, p, g[l + 14], 17, 2792965006), v, h, g[l + 15], 22, 1236535329), m = r(m, v = r(v, h = r(h, p, m, v, g[l + 1], 5, 4129170786), p, m, g[l + 6], 9, 3225465664), h, p, g[l + 11], 14, 643717713), v, h, g[l + 0], 20, 3921069994), m = r(m, v = r(v, h = r(h, p, m, v, g[l + 5], 5, 3593408605), p, m, g[l + 10], 9, 38016083), h, p, g[l + 15], 14, 3634488961), v, h, g[l + 4], 20, 3889429448), m = r(m, v = r(v, h = r(h, p, m, v, g[l + 9], 5, 568446438), p, m, g[l + 14], 9, 3275163606), h, p, g[l + 3], 14, 4107603335), v, h, g[l + 8], 20, 1163531501), m = r(m, v = r(v, h = r(h, p, m, v, g[l + 13], 5, 2850285829), p, m, g[l + 2], 9, 4243563512), h, p, g[l + 7], 14, 1735328473), v, h, g[l + 12], 20, 2368359562), m = o(m, v = o(v, h = o(h, p, m, v, g[l + 5], 4, 4294588738), p, m, g[l + 8], 11, 2272392833), h, p, g[l + 11], 16, 1839030562), v, h, g[l + 14], 23, 4259657740), m = o(m, v = o(v, h = o(h, p, m, v, g[l + 1], 4, 2763975236), p, m, g[l + 4], 11, 1272893353), h, p, g[l + 7], 16, 4139469664), v, h, g[l + 10], 23, 3200236656), m = o(m, v = o(v, h = o(h, p, m, v, g[l + 13], 4, 681279174), p, m, g[l + 0], 11, 3936430074), h, p, g[l + 3], 16, 3572445317), v, h, g[l + 6], 23, 76029189), m = o(m, v = o(v, h = o(h, p, m, v, g[l + 9], 4, 3654602809), p, m, g[l + 12], 11, 3873151461), h, p, g[l + 15], 16, 530742520), v, h, g[l + 2], 23, 3299628645), m = s(m, v = s(v, h = s(h, p, m, v, g[l + 0], 6, 4096336452), p, m, g[l + 7], 10, 1126891415), h, p, g[l + 14], 15, 2878612391), v, h, g[l + 5], 21, 4237533241), m = s(m, v = s(v, h = s(h, p, m, v, g[l + 12], 6, 1700485571), p, m, g[l + 3], 10, 2399980690), h, p, g[l + 10], 15, 4293915773), v, h, g[l + 1], 21, 2240044497), m = s(m, v = s(v, h = s(h, p, m, v, g[l + 8], 6, 1873313359), p, m, g[l + 15], 10, 4264355552), h, p, g[l + 6], 15, 2734768916), v, h, g[l + 13], 21, 1309151649), m = s(m, v = s(v, h = s(h, p, m, v, g[l + 4], 6, 4149444226), p, m, g[l + 11], 10, 3174756917), h, p, g[l + 2], 15, 718787259), v, h, g[l + 9], 21, 3951481745),
                    h = n(h, u),
                    p = n(p, c),
                    m = n(m, d),
                    v = n(v, f);
                return (a(h) + a(p) + a(m) + a(v)).toLowerCase()
            }(i.token + "&" + a + "&" + s + "&" + n.data);
    result=l;
    """
    return js, timestamp


def generate_params(t, sign, page_number):
    """
    生成请求体所需的参数
    :param t: 由generate_js返回的时间戳
    :param sign: 服务器解释js生成的sign值
    :param page_number:  页码
    :return:
    """
    params = {
        "jsv": "2.5.0",
        "appKey": "12574478",
        "t": t,
        "sign": sign,
        "api": "mtop.taobao.idle.home.nextfresh",
        "v": "3.0",
        "type": "jsonp",
        "dataType": "jsonp",
        "callback": "mtopjsonp5",
        "data": """{"spmPrefix":"a2170.7897990.6801272.","trackName":"Feed1","needBanner":"true","abtag":"style_masonryLayouts_1.0_mamaAD","pageNumber":%s}""" % page_number
    }
    return params
