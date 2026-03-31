from abc import abstractclassmethod

import pandas as pd

if __name__ == '__main__':
    print("验证数据定义")


class Data:
    """数据定义基类，所有数据类必须继承此类"""

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__()
        if not hasattr(cls, 'TABLE_NAME'):
            raise TypeError(f"数据定义子类 {cls.__name__} 必须定义 [表名] TABLE_NAME")
        if not hasattr(cls, 'COLUMN_MAPPING'):
            raise TypeError(f"数据定义子类 {cls.__name__} 必须定义 [列映射] COLUMN_MAPPING")
        if not hasattr(cls, 'UNIQUE_KEY'):
            raise TypeError(f"数据定义子类 {cls.__name__} 必须定义 [唯一键] UNIQUE_KEY")
        if not hasattr(cls, 'CREATE_TABLE_SQL'):
            raise TypeError(f"数据定义子类 {cls.__name__} 必须定义 [建表语句] CREATE_TABLE_SQL")

    def dealAndStorage(self, rs):
        rows = [rs.get_row_data() for _ in iter(rs.next, False)]
        df = (pd.DataFrame(rows, columns=rs.fields)
              .rename(columns=self.COLUMN_MAPPING)
              .set_index(self.UNIQUE_KEY))
        return df


# ==================== 4 获取历史A股K线数据 ====================

## ==================== 不复权 ====================

class HistoryKDataPlusMonth(Data):
    """历史A股K线数据_月线"""
    TABLE_NAME = "K线_月"
    COLUMN_MAPPING = {
        'date': '交易所行情日期',
        'code': '证券代码',
        'open': '开盘价格',
        'high': '最高价',
        'low': '最低价',
        'close': '收盘价',
        'volume': '成交数量',
        'amount': '成交金额',
        'adjustflag': '复权状态',
        'turn': '换手率',
        'pctChg': '涨跌幅'
    }
    UNIQUE_KEY = ['证券代码']
    CREATE_TABLE_SQL = f"""
    CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
        交易所行情日期   DATE,
        证券代码         VARCHAR(255),
        开盘价格         DECIMAL(10,4),
        最高价           DECIMAL(10,4),
        最低价           DECIMAL(10,4),
        收盘价           DECIMAL(10,4),
        成交数量         BIGINT,
        成交金额         DECIMAL(20,4),
        复权状态         INT COMMENT '1:后复权, 2:前复权, 3:不复权',
        换手率           DECIMAL(10,6),
        涨跌幅           DECIMAL(10,6),
        PRIMARY KEY (证券代码, 交易所行情日期)
    );"""


class HistoryKDataPlusWeek(Data):
    """历史A股K线数据_周线"""
    TABLE_NAME = "K线_周"
    COLUMN_MAPPING = {
        'date': '交易所行情日期',
        'code': '证券代码',
        'open': '开盘价格',
        'high': '最高价',
        'low': '最低价',
        'close': '收盘价',
        'volume': '成交数量',
        'amount': '成交金额',
        'adjustflag': '复权状态',
        'turn': '换手率',
        'pctChg': '涨跌幅'
    }
    UNIQUE_KEY = ['证券代码', '交易所行情日期']
    CREATE_TABLE_SQL = f"""
    CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
        交易所行情日期   DATE,
        证券代码         VARCHAR(255),
        开盘价格         DECIMAL(10,4),
        最高价           DECIMAL(10,4),
        最低价           DECIMAL(10,4),
        收盘价           DECIMAL(10,4),
        成交数量         BIGINT,
        成交金额         DECIMAL(20,4),
        复权状态         INT COMMENT '1:后复权, 2:前复权, 3:不复权',
        换手率           DECIMAL(10,6),
        涨跌幅           DECIMAL(10,6),
        PRIMARY KEY (证券代码, 交易所行情日期)
    );"""


class HistoryKDataPlusDaily(Data):
    """历史A股K线数据_日线"""
    TABLE_NAME = "K线_日"
    COLUMN_MAPPING = {
        'date': '交易所行情日期',
        'code': '证券代码',
        'open': '今开盘价格',
        'high': '最高价',
        'low': '最低价',
        'close': '今收盘价',
        'preclose': '昨日收盘价',
        'volume': '成交数量',
        'amount': '成交金额',
        'adjustflag': '复权状态',
        'turn': '换手率',
        'tradestatus': '交易状态',
        'pctChg': '涨跌幅',
        'peTTM': '滚动市盈率',
        'psTTM': '滚动市销率',
        'pcfNcfTTM': '滚动市现率',
        'pbMRQ': '市净率',
        'isST': '是否ST股'
    }
    UNIQUE_KEY = ['证券代码', '交易所行情日期']
    CREATE_TABLE_SQL = f"""
    CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
        交易所行情日期   DATE,
        证券代码         VARCHAR(255),
        今开盘价格       DECIMAL(10,4),
        最高价           DECIMAL(10,4),
        最低价           DECIMAL(10,4),
        今收盘价         DECIMAL(10,4),
        昨日收盘价       DECIMAL(10,4),
        成交数量         BIGINT,
        成交金额         DECIMAL(20,4),
        复权状态         INT COMMENT '1:后复权, 2:前复权, 3:不复权',
        换手率           DECIMAL(10,6),
        交易状态         INT COMMENT '1:正常交易, 0:停牌',
        涨跌幅           DECIMAL(10,6),
        滚动市盈率       DECIMAL(10,6),
        滚动市销率       DECIMAL(10,6),
        滚动市现率       DECIMAL(10,6),
        市净率           DECIMAL(10,6),
        是否ST股         INT COMMENT '1:是, 0:否',
        PRIMARY KEY (证券代码, 交易所行情日期)
    );"""


class HistoryKDataPlusHour(Data):
    """历史A股K线数据_小时线"""
    TABLE_NAME = "K线_分钟_60"
    COLUMN_MAPPING = {
        'date': '交易所行情日期',
        'time': '交易所行情时间',
        'code': '证券代码',
        'open': '开盘价格',
        'high': '最高价',
        'low': '最低价',
        'close': '收盘价',
        'volume': '成交数量',
        'amount': '成交金额',
        'adjustflag': '复权状态'
    }
    UNIQUE_KEY = ['证券代码', '交易所行情日期', '交易所行情时间']
    CREATE_TABLE_SQL = f"""
    CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
        交易所行情日期   DATE,
        交易所行情时间   VARCHAR(20),
        证券代码         VARCHAR(255),
        开盘价格         DECIMAL(10,4),
        最高价           DECIMAL(10,4),
        最低价           DECIMAL(10,4),
        收盘价           DECIMAL(10,4),
        成交数量         BIGINT,
        成交金额         DECIMAL(20,4),
        复权状态         INT COMMENT '1:后复权, 2:前复权, 3:不复权',
        PRIMARY KEY (证券代码, 交易所行情日期, 交易所行情时间)
    );"""


class HistoryKDataPlus30Min(Data):
    """历史A股K线数据_半小时线"""
    TABLE_NAME = "K线_分钟_30"
    COLUMN_MAPPING = {
        'date': '交易所行情日期',
        'time': '交易所行情时间',
        'code': '证券代码',
        'open': '开盘价格',
        'high': '最高价',
        'low': '最低价',
        'close': '收盘价',
        'volume': '成交数量',
        'amount': '成交金额',
        'adjustflag': '复权状态'
    }
    UNIQUE_KEY = ['证券代码', '交易所行情日期', '交易所行情时间']
    CREATE_TABLE_SQL = f"""
    CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
        交易所行情日期   DATE,
        交易所行情时间   VARCHAR(20),
        证券代码         VARCHAR(255),
        开盘价格         DECIMAL(10,4),
        最高价           DECIMAL(10,4),
        最低价           DECIMAL(10,4),
        收盘价           DECIMAL(10,4),
        成交数量         BIGINT,
        成交金额         DECIMAL(20,4),
        复权状态         INT COMMENT '1:后复权, 2:前复权, 3:不复权',
        PRIMARY KEY (证券代码, 交易所行情日期, 交易所行情时间)
    );"""


class HistoryKDataPlus15Min(Data):
    """历史A股K线数据_15分钟线"""
    TABLE_NAME = "K线_分钟_15"
    COLUMN_MAPPING = {
        'date': '交易所行情日期',
        'time': '交易所行情时间',
        'code': '证券代码',
        'open': '开盘价格',
        'high': '最高价',
        'low': '最低价',
        'close': '收盘价',
        'volume': '成交数量',
        'amount': '成交金额',
        'adjustflag': '复权状态'
    }
    UNIQUE_KEY = ['证券代码', '交易所行情日期', '交易所行情时间']
    CREATE_TABLE_SQL = f"""
    CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
        交易所行情日期   DATE,
        交易所行情时间   VARCHAR(20),
        证券代码         VARCHAR(255),
        开盘价格         DECIMAL(10,4),
        最高价           DECIMAL(10,4),
        最低价           DECIMAL(10,4),
        收盘价           DECIMAL(10,4),
        成交数量         BIGINT,
        成交金额         DECIMAL(20,4),
        复权状态         INT COMMENT '1:后复权, 2:前复权, 3:不复权',
        PRIMARY KEY (证券代码, 交易所行情日期, 交易所行情时间)
    );"""


class HistoryKDataPlus5Min(Data):
    """历史A股K线数据_分钟线"""
    TABLE_NAME = "K线_分钟_5"
    COLUMN_MAPPING = {
        'date': '交易所行情日期',
        'time': '交易所行情时间',
        'code': '证券代码',
        'open': '开盘价格',
        'high': '最高价',
        'low': '最低价',
        'close': '收盘价',
        'volume': '成交数量',
        'amount': '成交金额',
        'adjustflag': '复权状态'
    }
    UNIQUE_KEY = ['证券代码', '交易所行情日期', '交易所行情时间']
    CREATE_TABLE_SQL = f"""
    CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
        交易所行情日期   DATE,
        交易所行情时间   VARCHAR(20),
        证券代码         VARCHAR(255),
        开盘价格         DECIMAL(10,4),
        最高价           DECIMAL(10,4),
        最低价           DECIMAL(10,4),
        收盘价           DECIMAL(10,4),
        成交数量         BIGINT,
        成交金额         DECIMAL(20,4),
        复权状态         INT COMMENT '1:后复权, 2:前复权, 3:不复权',
        PRIMARY KEY (证券代码, 交易所行情日期, 交易所行情时间)
    );"""


# ==================== 5 查询除权除息信息 ====================

class DividendData(Data):
    """除权除息信息"""
    TABLE_NAME = "除权除息"
    COLUMN_MAPPING = {
        'code': '证券代码',
        'dividPreNoticeDate': '预披露公告日',
        'dividAgmPumDate': '股东大会公告日期',
        'dividPlanAnnounceDate': '预案公告日',
        'dividPlanDate': '分红实施公告日',
        'dividRegistDate': '股权登记日',
        'dividOperateDate': '除权除息日期',
        'dividPayDate': '派息日',
        'dividStockMarketDate': '红股上市交易日',
        'dividCashPsBeforeTax': '每股股利税前',
        'dividCashPsAfterTax': '每股股利税后',
        'dividStocksPs': '每股红股',
        'dividCashStock': '分红送转',
        'dividReserveToStockPs': '每股转增资本'
    }
    UNIQUE_KEY = ['证券代码', '年份']
    CREATE_TABLE_SQL = f"""
    CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
        证券代码         VARCHAR(255),
        年份             INT,
        预披露公告日     DATE,
        股东大会公告日期 DATE,
        预案公告日       DATE,
        分红实施公告日   DATE,
        股权登记日       DATE,
        除权除息日期     DATE,
        派息日           DATE,
        红股上市交易日   DATE,
        每股股利税前     DECIMAL(10,6),
        每股股利税后     VARCHAR(50),
        每股红股         DECIMAL(10,6),
        分红送转         VARCHAR(255),
        每股转增资本     DECIMAL(10,6),
        PRIMARY KEY (证券代码, 年份)
    );"""


# ==================== 6 查询复权因子信息 ====================

class AdjustFactor(Data):
    """复权因子信息"""
    TABLE_NAME = "复权因子"
    COLUMN_MAPPING = {
        'code': '证券代码',
        'dividOperateDate': '除权除息日期',
        'foreAdjustFactor': '向前复权因子',
        'backAdjustFactor': '向后复权因子',
        'adjustFactor': '本次复权因子'
    }
    UNIQUE_KEY = ['证券代码', '除权除息日期']
    CREATE_TABLE_SQL = f"""
    CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
        证券代码         VARCHAR(255),
        除权除息日期     DATE,
        向前复权因子     DECIMAL(15,6),
        向后复权因子     DECIMAL(15,6),
        本次复权因子     DECIMAL(15,6),
        PRIMARY KEY (证券代码, 除权除息日期)
    );"""


# ==================== 7 查询季频财务数据信息 ====================

class ProfitData(Data):
    """季频盈利能力"""
    TABLE_NAME = "季频盈利能力"
    COLUMN_MAPPING = {
        'code': '证券代码',
        'pubDate': '财报发布日期',
        'statDate': '财报统计日期',
        'roeAvg': '净资产收益率平均',
        'npMargin': '销售净利率',
        'gpMargin': '销售毛利率',
        'netProfit': '净利润',
        'epsTTM': '每股收益',
        'MBRevenue': '主营营业收入',
        'totalShare': '总股本',
        'liqaShare': '流通股本'
    }
    UNIQUE_KEY = ['证券代码', '财报统计日期']
    CREATE_TABLE_SQL = f"""
    CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
        证券代码             VARCHAR(255),
        财报发布日期         DATE,
        财报统计日期         DATE,
        净资产收益率平均     DECIMAL(10,6),
        销售净利率           DECIMAL(10,6),
        销售毛利率           DECIMAL(10,6),
        净利润               DECIMAL(20,2),
        每股收益             DECIMAL(10,6),
        主营营业收入         DECIMAL(20,2),
        总股本               DECIMAL(20,2),
        流通股本             DECIMAL(20,2),
        PRIMARY KEY (证券代码, 财报统计日期)
    );"""


class OperationData(Data):
    """季频营运能力"""
    TABLE_NAME = "季频营运能力"
    COLUMN_MAPPING = {
        'code': '证券代码',
        'pubDate': '财报发布日期',
        'statDate': '财报统计日期',
        'NRTurnRatio': '应收账款周转率',
        'NRTurnDays': '应收账款周转天数',
        'INVTurnRatio': '存货周转率',
        'INVTurnDays': '存货周转天数',
        'CATurnRatio': '流动资产周转率',
        'AssetTurnRatio': '总资产周转率'
    }
    UNIQUE_KEY = ['证券代码', '财报统计日期']
    CREATE_TABLE_SQL = f"""
    CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
        证券代码             VARCHAR(255),
        财报发布日期         DATE,
        财报统计日期         DATE,
        应收账款周转率       DECIMAL(10,6),
        应收账款周转天数     DECIMAL(10,2),
        存货周转率           DECIMAL(10,6),
        存货周转天数         DECIMAL(10,2),
        流动资产周转率       DECIMAL(10,6),
        总资产周转率         DECIMAL(10,6),
        PRIMARY KEY (证券代码, 财报统计日期)
    );"""


class GrowthData(Data):
    """季频成长能力"""
    TABLE_NAME = "季频成长能力"
    COLUMN_MAPPING = {
        'code': '证券代码',
        'pubDate': '财报发布日期',
        'statDate': '财报统计日期',
        'YOYEquity': '净资产同比增长率',
        'YOYAsset': '总资产同比增长率',
        'YOYNI': '净利润同比增长率',
        'YOYEPSBasic': '基本每股收益同比增长率',
        'YOYPNI': '归属母公司股东净利润同比增长率'
    }
    UNIQUE_KEY = ['证券代码', '财报统计日期']
    CREATE_TABLE_SQL = f"""
    CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
        证券代码                         VARCHAR(255),
        财报发布日期                     DATE,
        财报统计日期                     DATE,
        净资产同比增长率                 DECIMAL(10,6),
        总资产同比增长率                 DECIMAL(10,6),
        净利润同比增长率                 DECIMAL(10,6),
        基本每股收益同比增长率           DECIMAL(10,6),
        归属母公司股东净利润同比增长率   DECIMAL(10,6),
        PRIMARY KEY (证券代码, 财报统计日期)
    );"""


class BalanceData(Data):
    """季频偿债能力"""
    TABLE_NAME = "季频偿债能力"
    COLUMN_MAPPING = {
        'code': '证券代码',
        'pubDate': '财报发布日期',
        'statDate': '财报统计日期',
        'currentRatio': '流动比率',
        'quickRatio': '速动比率',
        'cashRatio': '现金比率',
        'YOYLiability': '总负债同比增长率',
        'liabilityToAsset': '资产负债率',
        'assetToEquity': '权益乘数'
    }
    UNIQUE_KEY = ['证券代码', '财报统计日期']
    CREATE_TABLE_SQL = f"""
    CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
        证券代码             VARCHAR(255),
        财报发布日期         DATE,
        财报统计日期         DATE,
        流动比率             DECIMAL(10,6),
        速动比率             DECIMAL(10,6),
        现金比率             DECIMAL(10,6),
        总负债同比增长率     DECIMAL(10,6),
        资产负债率           DECIMAL(10,6),
        权益乘数             DECIMAL(10,6),
        PRIMARY KEY (证券代码, 财报统计日期)
    );"""


class CashFlowData(Data):
    """季频现金流量"""
    TABLE_NAME = "季频现金流量"
    COLUMN_MAPPING = {
        'code': '证券代码',
        'pubDate': '财报发布日期',
        'statDate': '财报统计日期',
        'CAToAsset': '流动资产除以总资产',
        'NCAToAsset': '非流动资产除以总资产',
        'tangibleAssetToAsset': '有形资产除以总资产',
        'ebitToInterest': '已获利息倍数',
        'CFOToOR': '经营活动现金流量净额除以营业收入',
        'CFOToNP': '经营性现金净流量除以净利润',
        'CFOToGr': '经营性现金净流量除以营业总收入'
    }
    UNIQUE_KEY = ['证券代码', '财报统计日期']
    CREATE_TABLE_SQL = f"""
    CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
        证券代码                             VARCHAR(255),
        财报发布日期                         DATE,
        财报统计日期                         DATE,
        流动资产除以总资产                   DECIMAL(10,6),
        非流动资产除以总资产                 DECIMAL(10,6),
        有形资产除以总资产                   DECIMAL(10,6),
        已获利息倍数                         DECIMAL(10,6),
        经营活动现金流量净额除以营业收入     DECIMAL(10,6),
        经营性现金净流量除以净利润           DECIMAL(10,6),
        经营性现金净流量除以营业总收入       DECIMAL(10,6),
        PRIMARY KEY (证券代码, 财报统计日期)
    );"""


class DupontData(Data):
    """季频杜邦指数"""
    TABLE_NAME = "季频杜邦指数"
    COLUMN_MAPPING = {
        'code': '证券代码',
        'pubDate': '财报发布日期',
        'statDate': '财报统计日期',
        'dupontROE': '净资产收益率',
        'dupontAssetStoEquity': '权益乘数',
        'dupontAssetTurn': '总资产周转率',
        'dupontPnitoni': '归属母公司净利润占比',
        'dupontNitogr': '净利润除以营业总收入',
        'dupontTaxBurden': '净利润除以利润总额',
        'dupontIntburden': '利润总额除以息税前利润',
        'dupontEbittogr': '息税前利润除以营业总收入'
    }
    UNIQUE_KEY = ['证券代码', '财报统计日期']
    CREATE_TABLE_SQL = f"""
    CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
        证券代码                     VARCHAR(255),
        财报发布日期                 DATE,
        财报统计日期                 DATE,
        净资产收益率                 DECIMAL(10,6),
        权益乘数                     DECIMAL(10,6),
        总资产周转率                 DECIMAL(10,6),
        归属母公司净利润占比         DECIMAL(10,6),
        净利润除以营业总收入         DECIMAL(10,6),
        净利润除以利润总额           DECIMAL(10,6),
        利润总额除以息税前利润       DECIMAL(10,6),
        息税前利润除以营业总收入     DECIMAL(10,6),
        PRIMARY KEY (证券代码, 财报统计日期)
    );"""


# ==================== 8 查询季频公司报告信息 ====================

class PerformanceExpressReport(Data):
    """季频公司业绩快报"""
    TABLE_NAME = "季频业绩快报"
    COLUMN_MAPPING = {
        'code': '证券代码',
        'performanceExpPubDate': '业绩快报披露日',
        'performanceExpStatDate': '业绩快报统计日期',
        'performanceExpUpdateDate': '业绩快报更新日期',
        'performanceExpressTotalAsset': '业绩快报总资产',
        'performanceExpressNetAsset': '业绩快报净资产',
        'performanceExpressEPSChgPct': '业绩每股收益增长率',
        'performanceExpressROEWa': '业绩快报净资产收益率加权',
        'performanceExpressEPSDiluted': '业绩快报每股收益摊薄',
        'performanceExpressGRYOY': '业绩快报营业总收入同比',
        'performanceExpressOPYOY': '业绩快报营业利润同比'
    }
    UNIQUE_KEY = ['证券代码', '业绩快报统计日期']
    CREATE_TABLE_SQL = f"""
    CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
        证券代码                     VARCHAR(255),
        业绩快报披露日               DATE,
        业绩快报统计日期             DATE,
        业绩快报更新日期             DATE,
        业绩快报总资产               DECIMAL(20,2),
        业绩快报净资产               DECIMAL(20,2),
        业绩每股收益增长率           DECIMAL(10,6),
        业绩快报净资产收益率加权     DECIMAL(10,6),
        业绩快报每股收益摊薄         DECIMAL(10,6),
        业绩快报营业总收入同比       DECIMAL(10,6),
        业绩快报营业利润同比         DECIMAL(10,6),
        PRIMARY KEY (证券代码, 业绩快报统计日期)
    );"""


class ForecastReport(Data):
    """季频公司业绩预告"""
    TABLE_NAME = "季频业绩预告"
    COLUMN_MAPPING = {
        'code': '证券代码',
        'profitForcastExpPubDate': '业绩预告发布日期',
        'profitForcastExpStatDate': '业绩预告统计日期',
        'profitForcastType': '业绩预告类型',
        'profitForcastAbstract': '业绩预告摘要',
        'profitForcastChgPctUp': '预告净利润增长上限',
        'profitForcastChgPctDwn': '预告净利润增长下限'
    }
    UNIQUE_KEY = ['证券代码', '业绩预告统计日期']
    CREATE_TABLE_SQL = f"""
    CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
        证券代码             VARCHAR(255),
        业绩预告发布日期     DATE,
        业绩预告统计日期     DATE,
        业绩预告类型         VARCHAR(50),
        业绩预告摘要         TEXT,
        预告净利润增长上限   DECIMAL(10,6),
        预告净利润增长下限   DECIMAL(10,6),
        PRIMARY KEY (证券代码, 业绩预告统计日期)
    );"""


# ==================== 9 证券基本资料 ====================

class StockBasic(Data):
    """证券基本资料"""
    TABLE_NAME = "证券基本资料"
    COLUMN_MAPPING = {
        'code': '证券代码',
        'code_name': '证券名称',
        'ipoDate': '上市日期',
        'outDate': '退市日期',
        'type': '证券类型',
        'status': '上市状态'
    }
    UNIQUE_KEY = ['证券代码']
    CREATE_TABLE_SQL = f"""
    CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
        证券代码     VARCHAR(255) PRIMARY KEY,
        证券名称     VARCHAR(255),
        上市日期     DATE,
        退市日期     DATE,
        证券类型     INT COMMENT '1:股票, 2:指数, 3:其它, 4:可转债, 5:ETF',
        上市状态     INT COMMENT '1:上市, 0:退市'
    );"""


# ==================== 10 获取证券元信息 ====================

class TradeDates(Data):
    """交易日查询"""
    TABLE_NAME = "交易日历"
    COLUMN_MAPPING = {
        'calendar_date': '日期',
        'is_trading_day': '是否交易日'
    }
    UNIQUE_KEY = ['日期']
    CREATE_TABLE_SQL = f"""
    CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
        日期         DATE PRIMARY KEY,
        是否交易日   INT COMMENT '0:非交易日, 1:交易日'
    );"""


class AllStock(Data):
    """证券代码查询（全部证券列表）"""
    TABLE_NAME = "证券代码列表"
    COLUMN_MAPPING = {
        'code': '证券代码',
        'code_name': '证券名称',
        'tradeStatus': '交易状态'
    }
    UNIQUE_KEY = ['证券代码']
    CREATE_TABLE_SQL = f"""
    CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
        证券代码     VARCHAR(255) PRIMARY KEY,
        证券名称     VARCHAR(255),
        交易状态     INT COMMENT '1:正常交易, 0:停牌'
    );"""


# ==================== 11 宏观经济数据 ====================

class DepositRateData(Data):
    """存款利率"""
    TABLE_NAME = "存款利率"
    COLUMN_MAPPING = {
        'pubDate': '发布日期',
        'demandDepositRate': '活期存款',
        'fixedDepositRate3Month': '定期存款三个月',
        'fixedDepositRate6Month': '定期存款半年',
        'fixedDepositRate1Year': '定期存款一年',
        'fixedDepositRate2Year': '定期存款二年',
        'fixedDepositRate3Year': '定期存款三年',
        'fixedDepositRate5Year': '定期存款五年',
        'installmentFixedDepositRate1Year': '零存整取一年',
        'installmentFixedDepositRate3Year': '零存整取三年',
        'installmentFixedDepositRate5Year': '零存整取五年'
    }
    UNIQUE_KEY = ['发布日期']
    CREATE_TABLE_SQL = f"""
    CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
        发布日期             DATE PRIMARY KEY,
        活期存款             DECIMAL(10,6),
        定期存款三个月       DECIMAL(10,6),
        定期存款半年         DECIMAL(10,6),
        定期存款一年         DECIMAL(10,6),
        定期存款二年         DECIMAL(10,6),
        定期存款三年         DECIMAL(10,6),
        定期存款五年         DECIMAL(10,6),
        零存整取一年         DECIMAL(10,6),
        零存整取三年         DECIMAL(10,6),
        零存整取五年         DECIMAL(10,6)
    );"""


class LoanRateData(Data):
    """贷款利率"""
    TABLE_NAME = "贷款利率"
    COLUMN_MAPPING = {
        'pubDate': '发布日期',
        'loanRate6Month': '六个月贷款利率',
        'loanRate6MonthTo1Year': '六个月至一年贷款利率',
        'loanRate1YearTo3Year': '一年至三年贷款利率',
        'loanRate3YearTo5Year': '三年至五年贷款利率',
        'loanRateAbove5Year': '五年以上贷款利率',
        'mortgateRateBelow5Year': '五年以下公积金贷款利率',
        'mortgateRateAbove5Year': '五年以上公积金贷款利率'
    }
    UNIQUE_KEY = ['发布日期']
    CREATE_TABLE_SQL = f"""
    CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
        发布日期                 DATE PRIMARY KEY,
        六个月贷款利率           DECIMAL(10,6),
        六个月至一年贷款利率     DECIMAL(10,6),
        一年至三年贷款利率       DECIMAL(10,6),
        三年至五年贷款利率       DECIMAL(10,6),
        五年以上贷款利率         DECIMAL(10,6),
        五年以下公积金贷款利率   DECIMAL(10,6),
        五年以上公积金贷款利率   DECIMAL(10,6)
    );"""


class RequiredReserveRatioData(Data):
    """存款准备金率"""
    TABLE_NAME = "存款准备金率"
    COLUMN_MAPPING = {
        'pubDate': '公告日期',
        'effectiveDate': '生效日期',
        'bigInstitutionsRatioPre': '大型金融机构调整前',
        'bigInstitutionsRatioAfter': '大型金融机构调整后',
        'mediumInstitutionsRatioPre': '中小型金融机构调整前',
        'mediumInstitutionsRatioAfter': '中小型金融机构调整后'
    }
    UNIQUE_KEY = ['公告日期']
    CREATE_TABLE_SQL = f"""
    CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
        公告日期                 DATE PRIMARY KEY,
        生效日期                 DATE,
        大型金融机构调整前       DECIMAL(10,2),
        大型金融机构调整后       DECIMAL(10,2),
        中小型金融机构调整前     DECIMAL(10,2),
        中小型金融机构调整后     DECIMAL(10,2)
    );"""


class MoneySupplyDataMonth(Data):
    """货币供应量（月度）"""
    TABLE_NAME = "货币供应量_月"
    COLUMN_MAPPING = {
        'statYear': '统计年度',
        'statMonth': '统计月份',
        'm0Month': '货币供应量M0',
        'm0YOY': '货币供应量M0同比',
        'm0ChainRelative': '货币供应量M0环比',
        'm1Month': '货币供应量M1',
        'm1YOY': '货币供应量M1同比',
        'm1ChainRelative': '货币供应量M1环比',
        'm2Month': '货币供应量M2',
        'm2YOY': '货币供应量M2同比',
        'm2ChainRelative': '货币供应量M2环比'
    }
    UNIQUE_KEY = ['统计年度', '统计月份']
    CREATE_TABLE_SQL = f"""
    CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
        统计年度             INT,
        统计月份             INT,
        货币供应量M0         DECIMAL(20,2),
        货币供应量M0同比     DECIMAL(10,6),
        货币供应量M0环比     DECIMAL(10,6),
        货币供应量M1         DECIMAL(20,2),
        货币供应量M1同比     DECIMAL(10,6),
        货币供应量M1环比     DECIMAL(10,6),
        货币供应量M2         DECIMAL(20,2),
        货币供应量M2同比     DECIMAL(10,6),
        货币供应量M2环比     DECIMAL(10,6),
        PRIMARY KEY (统计年度, 统计月份)
    );"""


class MoneySupplyDataYear(Data):
    """货币供应量（年底余额）"""
    TABLE_NAME = "货币供应量年底余额"
    COLUMN_MAPPING = {
        'statYear': '统计年度',
        'm0Year': '年货币供应量M0',
        'm0YearYOY': '年货币供应量M0同比',
        'm1Year': '年货币供应量M1',
        'm1YearYOY': '年货币供应量M1同比',
        'm2Year': '年货币供应量M2',
        'm2YearYOY': '年货币供应量M2同比'
    }
    UNIQUE_KEY = ['统计年度']
    CREATE_TABLE_SQL = f"""
    CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
        统计年度             INT PRIMARY KEY,
        年货币供应量M0       DECIMAL(20,2),
        年货币供应量M0同比   DECIMAL(10,6),
        年货币供应量M1       DECIMAL(20,2),
        年货币供应量M1同比   DECIMAL(10,6),
        年货币供应量M2       DECIMAL(20,2),
        年货币供应量M2同比   DECIMAL(10,6)
    );"""


# ==================== 板块数据 ====================

class StockIndustry(Data):
    """行业分类"""
    TABLE_NAME = "行业分类"
    COLUMN_MAPPING = {
        'code': '证券代码',
        'code_name': '证券名称',
        'industry': '所属行业',
        'industryClassification': '所属行业类别',
        'updateDate': '更新日期'
    }
    UNIQUE_KEY = ['证券代码']
    CREATE_TABLE_SQL = f"""
    CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
        证券代码         VARCHAR(255) PRIMARY KEY,
        证券名称         VARCHAR(255),
        所属行业         VARCHAR(255),
        所属行业类别     VARCHAR(255),
        更新日期         DATE
    );"""


class Sz50Stocks(Data):
    """上证50成分股"""
    TABLE_NAME = "上证50成分股"
    COLUMN_MAPPING = {
        'code': '证券代码',
        'code_name': '证券名称',
        'updateDate': '更新日期'
    }
    UNIQUE_KEY = ['证券代码']
    CREATE_TABLE_SQL = f"""
    CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
        证券代码     VARCHAR(255) PRIMARY KEY,
        证券名称     VARCHAR(255),
        更新日期     DATE
    );"""


class Hs300Stocks(Data):
    """沪深300成分股"""
    TABLE_NAME = "沪深300成分股"
    COLUMN_MAPPING = {
        'code': '证券代码',
        'code_name': '证券名称',
        'updateDate': '更新日期'
    }
    UNIQUE_KEY = ['证券代码']
    CREATE_TABLE_SQL = f"""
    CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
        证券代码     VARCHAR(255) PRIMARY KEY,
        证券名称     VARCHAR(255),
        更新日期     DATE
    );"""


class Zz500Stocks(Data):
    """中证500成分股"""
    TABLE_NAME = "中证500成分股"
    COLUMN_MAPPING = {
        'code': '证券代码',
        'code_name': '证券名称',
        'updateDate': '更新日期'
    }
    UNIQUE_KEY = ['证券代码']
    CREATE_TABLE_SQL = f"""
    CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
        证券代码     VARCHAR(255) PRIMARY KEY,
        证券名称     VARCHAR(255),
        更新日期     DATE
    );"""
