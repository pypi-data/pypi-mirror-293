#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project ：DfLangParser
@File    ：CharWorker.py
@Author  ：zhenxi_zhang@cx
@Date    ：2024/8/29 上午10:05
@explain : 文件说明
"""
# %%
import pandas as pd


class CharWorker:
    """
    用于接收字符流中的单个字符串，并做相应处理，返回到解析器中
    """

    def __init__(self, symbol, root_parser, end_symbol=None):
        if end_symbol is None:
            end_symbol = [";", "(", ")"]
        self._symbol = symbol  # 设置字段标识
        self.loading_flag = False  # 用于指示是否触碰到字段标识
        self._mem = ""  # 缓存
        self.root_parser = root_parser  # 所属的解析器
        self._end_symbol = end_symbol

    def run(self, char):
        if not isinstance(char, str) or len(char) != 1:
            raise ValueError("Expected a single character string")
        if char in self._end_symbol:
            self._upload_string()
            self._mem += char
            self._upload_string()
            return
        if char == self._symbol:
            self.if_detected_symbol()
        else:
            self._mem += char
        return

    def if_detected_symbol(self):
        if self.loading_flag:
            # 如果已经是读取字段状态，则关闭读取状态，并上传字符串
            self.loading_flag = False
            self._upload_string()
            return
        else:
            # 说明此时仍未进入读取字段状态，如果缓存内容不为空，将缓存内容去空格上传，缓存内容应为运算符
            self.loading_flag = True
            if self._mem != "":
                self._mem = self._mem.strip()
                self._upload_string()
            return

    def _upload_string(self):
        if self._mem == "":
            return
        self._mem = self._mem.strip()
        self.root_parser.append2cache(self._mem)
        self._mem = ""

    def check_if_in_end_symbol(self, string):
        if string in self._end_symbol:
            return True
        else:
            return False


class LangParser:
    def __init__(self):
        self._relation_operator = ["==", "!=", "<", ">", "<=", ">="]
        self._numerical_operator = ["+", "-", "*", "/"]
        self._logical_operator = ["and", "or", "xor"]

        self._mem = []
        self._sentence_tmp = []
        self._opt_tmp = None

        self.cw = CharWorker('"', self)
        self.lang_type = None
        self.lang_type_flag = False

        self.status_code = 0
        self._status_barrier = 3

        self.df = pd.DataFrame()
        self.result = pd.DataFrame()

    def get_buffers(self, string):
        for char in string:
            self.cw.run(char)

    def append2cache(self, string):
        if not self.lang_type_flag:
            if string in self._relation_operator:
                self.lang_type = "DfFilter"
                self.lang_type_flag = True
            if string in self._numerical_operator:
                self.lang_type = "CalcFilter"
                self.lang_type_flag = True

        self._mem.append(string)
        if self.cw.check_if_in_end_symbol(string):
            return
        if string in self._logical_operator:
            self._opt_tmp = string
            return
        self._sentence_tmp.append(string)
        self.status_code += 1

        if self.status_code == self._status_barrier:
            if self.lang_type == "CalcFilter":
                self._status_barrier = 2
                self.df_calc(self._sentence_tmp)
            if self.lang_type == "DfFilter":
                self.df_filter_calc(self._sentence_tmp)
            self._sentence_tmp = []
            self.status_code = 0

    def _bind_df(self, df):
        self.df = df

    def run(self, string, df):
        self._bind_df(df)
        self.get_buffers(string)
        if self.lang_type is None:
            raise ValueError("未能解析语句类型，请检查运算符")
        return self.result

    def df_filter_calc(self, string):
        a = self.df[[string[0]]]
        b = string[2]
        opt = string[1]

        if opt == "==":
            tmp_res = a == b
        elif opt == "!=":
            tmp_res = a != b
        elif opt == "<":
            tmp_res = a < b
        elif opt == ">":
            tmp_res = a > b
        elif opt == "<=":
            tmp_res = a <= b
        elif opt == ">=":
            tmp_res = a >= b
        else:
            raise ValueError(f"不支持的运算符{opt}")
        tmp_res = tmp_res.values
        if self._opt_tmp is None:
            self.result = tmp_res
        elif self._opt_tmp == "and":
            self.result = self.result & tmp_res
        elif self._opt_tmp == "or":
            self.result = self.result | tmp_res
        elif self._opt_tmp == "xor":
            self.result = self.result ^ tmp_res

    def df_calc(self, string):
        def _test_type(_a):
            try:
                _a = float(_a)
            except ValueError:
                try:
                    _a = self.df[_a]
                except IndexError:
                    raise Exception(f"类型测试错误，非字段也不可转为浮点数 {_a}")
            return _a

        if len(string) == 3:
            a = _test_type(string[0])
            b = _test_type(string[2])
            opt = string[1]
        elif len(string) == 2:
            a = self.result
            b = _test_type(string[1])
            opt = string[0]
        else:
            raise ValueError("不支持的表达式")
        if opt == "+":
            self.result = a * b
        elif opt == "-":
            self.result = a - b
        elif opt == "*":
            self.result = a * b
        elif opt == "/":
            self.result = a / b
        else:
            raise ValueError(f"不支持的运算符{opt}")


if __name__ == "__main__":
    test = '("标的品种" != "外汇类") and ("跨境标识" == "Domestic") and ("标的市场" == "境外");'
    p = LangParser()
    p.run(test, df)

    test1 = '("估值日价格" - "期初价格") * "名义数量" * "合约乘数" * "我司方向";'
    p1 = LangParser()
    p1.run(test1, df)
