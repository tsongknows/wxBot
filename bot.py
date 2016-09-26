#!/usr/bin/env python
# coding: utf-8

from wxbot import *
import ConfigParser
import json


class TulingWXBot(WXBot):
    def __init__(self):
        WXBot.__init__(self)

        self.tuling_key = ""
        self.robot_switch = True

        try:
            cf = ConfigParser.ConfigParser()
            cf.read('conf.ini')
            self.tuling_key = cf.get('main', 'key')
        except Exception:
            pass
        print 'tuling_key:', self.tuling_key

    def tuling_auto_reply(self, uid, msg):
        if msg == u"sb":
            return u"你才sb, 发个红包先"

        if self.tuling_key:
            url = "http://www.tuling123.com/openapi/api"
            user_id = uid.replace('@', '')[:30]
            body = {'key': self.tuling_key, 'info': msg.encode('utf8'), 'userid': user_id}
            r = requests.post(url, data=body)
            respond = json.loads(r.text)
            result = ''
            if respond['code'] == 100000:
                result = respond['text'].replace('<br>', '  ')
            elif respond['code'] == 200000:
                result = respond['url']
            elif respond['code'] == 302000:
                for k in respond['list']:
                    result = result + u"【" + k['source'] + u"】 " +\
                        k['article'] + "\t" + k['detailurl'] + "\n"
            else:
                result = respond['text'].replace('<br>', '  ')

            print '    ROBOT:', result
            return result
        else:
            return u"知道啦"

    def auto_switch(self, msg):
        msg_data = msg['content']['data']
        stop_cmd = [u'退下', u'走开', u'关闭', u'关掉', u'休息', u'滚开']
        start_cmd = [u'出来', u'启动', u'工作']
        if self.robot_switch:
            for i in stop_cmd:
                if i == msg_data:
                    self.robot_switch = False
                    self.send_msg_by_uid(u'[Robot]' + u'机器人已关闭！', msg['to_user_id'])
        else:
            for i in start_cmd:
                if i == msg_data:
                    self.robot_switch = True
                    self.send_msg_by_uid(u'[Robot]' + u'机器人已开启！', msg['to_user_id'])

    def handle_msg_all(self, msg):
        self.addMessageToHistory(msg)

        if not self.robot_switch and msg['msg_type_id'] != 1:
            return

        msgType0 = msg['content']['type'] == 0
        if not msgType0:
            return

        if msg['msg_type_id'] == 1:  # reply to self
            self.auto_switch(msg)
        elif msg['msg_type_id'] == 4:  # text message from contact
            reply = self.tuling_auto_reply(msg['user']['id'], msg['content']['data']);
            self.send_msg_by_uid(reply, msg['user']['id'])
        elif msg['msg_type_id'] == 3:  # group text message
            if not 'detail' in msg['content']:
                return

            is_at_me = self.isAtMe(msg, self.getMyNames(msg))
            if not is_at_me:
                return

            src_name = msg['content']['user']['name']
            reply = 'to ' + src_name + ': '
            if msg['content']['type'] == 0:  # text message
                reply += self.tuling_auto_reply(msg['content']['user']['id'], msg['content']['desc'])
            else:
                reply += u"对不起，只认字，其他杂七杂八的我都不认识，,,Ծ‸Ծ,,"
            self.send_msg_by_uid(reply, msg['user']['id'])

    def getMyNames(self,msg):
        my_names = self.get_group_member_name(self.my_account['UserName'], msg['user']['id'])
        if my_names is None:
            my_names = {}
        if 'NickName' in self.my_account and self.my_account['NickName']:
            my_names['nickname2'] = self.my_account['NickName']
        if 'RemarkName' in self.my_account and self.my_account['RemarkName']:
            my_names['remark_name2'] = self.my_account['RemarkName']

        return my_names

    def isAtMe(self,msg,my_names):
        for detail in msg['content']['detail']:
            if detail['type'] == 'at':
                for k in my_names:
                    if my_names[k] and my_names[k] == detail['value']:
                        return True
        return False

def main():
    bot = TulingWXBot()
    bot.DEBUG = True
    bot.conf['qr'] = 'png'

    bot.run()


if __name__ == '__main__':
    main()

