#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'py-z'

import web, re
from alipay import Alipay
urls = (
    '/pay_url', 'pay_url', # 支付宝跳转连接
    '/pay_return', 'pay_return', # 支付成功同步通知
    '/pay_notify', 'pay_notify', # 异步通知
)

alipay = Alipay(pid='2088121864519546', key='diq8di50v4td7llajgdkc7lhwt3gh5al', seller_email='douzw888@163.com')

class pay_url:
    def GET(self):
        i = web.input()
        url = alipay.create_direct_pay_by_user_url(out_trade_no=i.get('out_trade_no'), subject=unicode(i.get('subject')), total_fee=i.get('total_fee'), return_url=web.ctx.get('homedomain')+'/pay_return'), notify_url=web.ctx.get('homedomain')+'/pay_notify')
        return web.seeother(url)

class pay_return:
    def GET(self):
        i = web.input()
        if alipay.check_notify_remotely(**i):
            # 支付成功同步处理逻辑
            # return 'ok'
            trade_no = i.get('out_trade_no') # 订单号
            total_fee = i.get('total_fee') # 交易金额
            return '支付成功 订单号%s, 交易金额%s' % (trade_no, total_fee)
        else:
            return u'验证失败!'


'''
返回数据
<Storage {'seller_email': u'douzw888@163.com', 'sign': u'a4d92db8333e3dec308b490958e0e48b', 'subject': u'\u5510\u5bb4\u6625,\u9879\u76ee\u5e73\u53f0\u652f\u4ed8\u5168\u90e8\u91d1\u989d', 'is_total_fee_adjust': u'N', 'gmt_create': u'2016-02-18 11:58:23', 'out_trade_no': u'68', 'sign_type': u'MD5', 'price': u'0.01', 'buyer_email': u'qiao-juan@qq.com', 'discount': u'0.00', 'trade_status': u'TRADE_SUCCESS', 'gmt_payment': u'2016-02-18 11:58:27', 'trade_no': u'2016021821001004720237786769', 'seller_id': u'2088121864519546', 'use_coupon': u'N', 'payment_type': u'1', 'total_fee': u'0.01', 'notify_time': u'2016-02-18 12:22:48', 'quantity': u'1', 'notify_id': u'1c11f6ed8d1b51e0bd0898cc53f4fc6lk2', 'notify_type': u'trade_status_sync', 'buyer_id': u'2088202454737721'}>
'''
class pay_notify:
    def POST(self):
        i = web.input()
        if alipay.verify_notify(**i):
            # 支付成功异步处理逻辑 补单
            return 'success'

application = web.application(urls, globals()).wsgifunc()
if __name__ == "__main__":
    WSGIServer(('', 4088), application).serve_forever()
