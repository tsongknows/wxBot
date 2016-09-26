#!/usr/bin/env python
# coding: utf-8

from wxbot import *


class MyWXBot(WXBot):
    def handle_msg_all(self, msg):
        print str(msg)
        self.addMessageToHistory(msg)
        content = msg['content']['data']
        if msg['msg_type_id'] == 4 and msg['content']['type'] == 0:
            self.send_msg_by_uid(u'hi', msg['user']['id'])
            #self.send_img_msg_by_uid("img/1.png", msg['user']['id'])
            #self.send_file_msg_by_uid("img/1.png", msg['user']['id'])
        elif msg['msg_type_id'] == 1 and msg['content']['type'] == 0:  # reply to self
            if content == u'开启':
                self.send_msg_by_uid(u'[Robot]' + u'机器人已开启！', msg['to_user_id'])
        elif msg['msg_type_id'] == 4 and msg['content']['type'] == 0:  # text message from contact
            self.send_msg_by_uid(msg['content']['data'], msg['user']['id'])
        elif msg['msg_type_id'] == 3:  # group text message
            if  msg['content']['type'] == 0:
                reply = content
            else:
                reply = u"对不起，只认字，其他杂七杂八的我都不认识，,,Ծ‸Ծ,,"
            self.send_msg_by_uid(reply, msg['user']['id'])
'''
    def schedule(self):
        self.send_msg(u'张三', u'测试')
        time.sleep(1)
'''


def main():
    bot = MyWXBot()
    bot.DEBUG = True
    bot.conf['qr'] = 'png'
    bot.run()


if __name__ == '__main__':
    main()
