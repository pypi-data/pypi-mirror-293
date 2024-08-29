#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：LockonTools 
@File    ：EmlReader.py
@Author  ：zhenxi_zhang@cx
@Date    ：2024/7/1 上午9:39 
@explain : 文件说明
'''

import email.header
import os
from email.parser import Parser
import json
import pandas as pd
from email.utils import parsedate_to_datetime


class MailReader(object):
    def __init__(self, eml_path="", debug=False):
        self.raw_email = None
        self.email_content = None
        self.process_log = ""
        self.debug = debug
        self.header_dict = {}
        self.mail_text = ""
        self.all_links = []
        self.date = ""
        if eml_path:
            self.__mail_reader(eml_path)
            self.eml_path = eml_path

    @staticmethod
    def decode_header(header_str):
        """
        输入需要解码的header字符串，返回解码结果
        """
        temp = email.header.decode_header(header_str)
        result = email.header.make_header(temp)
        return result

    def to_string(self):
        """
        打印整个邮件以及日志
        """
        print("email内容:", self.email_content)
        if self.debug:
            print("process_log:", self.process_log)
        return self.email_content

    def to_dict(self):
        """
        把header转换为字典形式,From,To,Subject需要单独解码
        """
        each_key: str

        if self.header_dict != {}:
            return self.header_dict

        for each_key in set(self.email_content.keys()):
            self.header_dict.update({each_key: self.email_content.get_all(each_key)})

        for each_key in ["From", "To", "Subject"]:
            temp = []
            for each_str in self.header_dict.get(each_key):
                each_str = str(self.decode_header(each_str))
                temp.append(each_str)
            self.header_dict.update({each_key: temp})
        return self.header_dict

    def to_json(self):
        """
        把header转换为json格式
        """
        if self.header_dict == {}:
            self.header_dict = self.to_dict()
        return json.dumps(self.header_dict)

    def __mail_reader(self, eml_path):
        """
        读取邮件
        """
        try:
            if os.path.exists(eml_path):
                with open(eml_path) as fp:
                    self.raw_email = fp.read()
                self.email_content = Parser().parsestr(self.raw_email)
                self.date = parsedate_to_datetime(
                    email.message_from_string(self.raw_email)["Date"]
                ).strftime("%Y%m%d")
                self.detailed_date = parsedate_to_datetime(email.message_from_string(self.raw_email)["Date"])
        except Exception as e:
            self.process_log += "读取邮件失败:" + str(e)
            self.to_string()
        return self

    def parse_mail(self, eml_path):
        """
        输入邮件路径，用email库整理邮件
        """
        self.header_dict = {}
        return self.__mail_reader(eml_path)

    def getContent(self):
        """
        循环遍历数据块并尝试解码,暂时只处理text数据
        """
        all_content = []
        for par in self.email_content.walk():
            if not par.is_multipart():  # 这里要判断是否是multipart，是的话，里面的数据是无用的
                str_charset = par.get_content_charset(failobj=None)  # 当前数据块的编码信息
                str_content_type = par.get_content_type()
                if str_content_type in ("text/plain", "text/html"):
                    content = par.get_payload(decode=True)
                    all_content.append(content.decode(str_charset))
        self.mail_text = all_content
        return all_content

    def getDFfromHTML(self):
        """ 用于获取正文中的表格HTML表格，确保正文中仅包含表格
        :return:pd.DataFrame
        """
        if self.email_content is None:
            return pd.DataFrame()
        email_message = email.message_from_string(self.email_content.as_string())
        body = ""
        if email_message.is_multipart():
            for part in email_message.walk():
                if part.get_content_type() == "text/html":
                    body = part.get_payload(decode=True)
                    break
        else:
            body = email_message.get_payload(decode=True)
        df = pd.read_html(body)[0]
        return df

    def getAttr(self, attr_dir):
        """
        用于获取附件，并且将附件保存在指定位置
        :return:
        :rtype:
        """
        for par in self.email_content.walk():
            if not par.is_multipart():  # 判断是否为multipart，里面的数据不需要
                name = par.get_param("name")  # 获取附件的文件名
                if name:
                    # 附件
                    fname = email.header.decode_header(name)[0]
                    if fname[1]:
                        attr_name = fname[0].decode(fname[1])
                    else:
                        attr_name = fname[0]
                    # # 解码附件内容
                    attr_data = par.get_payload(decode=True)
                    attr_fp = os.path.join(attr_dir, attr_name)
                    with open(attr_fp, 'wb') as f_write:
                        f_write.write(attr_data)
