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

class pay_notify:
    def POST(self):
        i = web.input()
        if alipay.verify_notify(**i):
            # 支付成功异步处理逻辑 补单
            notify_data = i.get('notify_data')
            trade_no = re.search('<trade_no>(.+)<\/trade_no>',notify_data).group(1) # 订单号
            total_free = re.search('<total_fee>(.+)<\/total_fee>',notify_data).group(1) # 交易金额
            return 'success'

application = web.application(urls, globals()).wsgifunc()
if __name__ == "__main__":
    WSGIServer(('', 4088), application).serve_forever()
