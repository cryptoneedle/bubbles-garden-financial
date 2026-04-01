import sys
from pathlib import Path

import pandas as pd
from sqlalchemy import MetaData, Table, Column, Integer, String, Date, Boolean, create_engine, Date
from pangres import upsert

sys.path.insert(0, str(Path(__file__).parent.parent))

from db.database import engine, schema

if __name__ == '__main__':
    print("验证数据定义")


class Data:
    """数据定义基类，所有数据类必须继承此类"""

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__()
        if not hasattr(cls, 'METADATA'):
            raise TypeError(f"数据定义子类 {cls.__name__} 必须定义 [元数据] METADATA")
        if not hasattr(cls, 'TABLE_NAME'):
            raise TypeError(f"数据定义子类 {cls.__name__} 必须定义 [表名] TABLE_NAME")
        if not hasattr(cls, 'TABLE_MATEDATA'):
            raise TypeError(f"数据定义子类 {cls.__name__} 必须定义 [表元数据] TABLE_MATEDATA")
        if not hasattr(cls, 'COLUMN_MAPPING'):
            raise TypeError(f"数据定义子类 {cls.__name__} 必须定义 [列映射] COLUMN_MAPPING")
        if not hasattr(cls, 'UNIQUE_KEY'):
            raise TypeError(f"数据定义子类 {cls.__name__} 必须定义 [唯一键] UNIQUE_KEY")

    @classmethod
    def transform(cls, df):
        """子类可重写此方法进行数据转换"""
        return df

    @classmethod
    def dealAndStorage(cls, rs, year=None, quarter=None, date=None):
        rows = [rs.get_row_data() for _ in iter(rs.next, False)] if rs.error_code == '0' else []

        df = (pd.DataFrame(rows, columns=rs.fields)
              .rename(columns=cls.COLUMN_MAPPING)
              .replace('', pd.NA)
              .pipe(cls.transform))

        if '年' in cls.UNIQUE_KEY:
            df = df.assign(年=year)
        if '季度' in cls.UNIQUE_KEY:
            df = df.assign(季度=quarter)
        if '日期' in cls.UNIQUE_KEY:
            df = df.assign(日期=date)

        df = df.set_index(cls.UNIQUE_KEY)

        # print("示例数据：\n", df.head(5))
        print("共获取：", len(rows), "共写入：", len(df))
        if len(rows) > 0:
            print("原数据示例：", rows[0])

        upsert(
            con=engine,
            df=df,
            schema=schema,
            table_name=cls.TABLE_NAME,
            if_row_exists='update',
            chunksize=10000
        )


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
    METADATA = MetaData()
    TABLE_MATEDATA = Table(
        TABLE_NAME,
        METADATA,
        Column('交易所行情日期', Date, primary_key=True),
        Column('证券代码', String(30), primary_key=True),
        Column('开盘价格', String(30)),
        Column('最高价', String(30)),
        Column('最低价', String(30)),
        Column('收盘价', String(30)),
        Column('成交数量', String(30)),
        Column('成交金额', String(30)),
        Column('复权状态', String(30)),
        Column('换手率', String(30)),
        Column('涨跌幅', String(30))
    )
    UNIQUE_KEY = ['证券代码', '交易所行情日期']


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
    METADATA = MetaData()
    TABLE_MATEDATA = Table(
        TABLE_NAME,
        METADATA,
        Column('交易所行情日期', Date, primary_key=True),
        Column('证券代码', String(30), primary_key=True),
        Column('开盘价格', String(30)),
        Column('最高价', String(30)),
        Column('最低价', String(30)),
        Column('收盘价', String(30)),
        Column('成交数量', String(30)),
        Column('成交金额', String(30)),
        Column('复权状态', String(30)),
        Column('换手率', String(30)),
        Column('涨跌幅', String(30))
    )
    UNIQUE_KEY = ['证券代码', '交易所行情日期']


class HistoryKDataPlusDay(Data):
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
    METADATA = MetaData()
    TABLE_MATEDATA = Table(
        TABLE_NAME,
        METADATA,
        Column('交易所行情日期', Date, primary_key=True),
        Column('证券代码', String(30), primary_key=True),
        Column('今开盘价格', String(30)),
        Column('最高价', String(30)),
        Column('最低价', String(30)),
        Column('今收盘价', String(30)),
        Column('昨日收盘价', String(30)),
        Column('成交数量', String(30)),
        Column('成交金额', String(30)),
        Column('复权状态', String(30)),
        Column('换手率', String(30)),
        Column('交易状态', String(30)),
        Column('涨跌幅', String(30)),
        Column('滚动市盈率', String(30)),
        Column('滚动市销率', String(30)),
        Column('滚动市现率', String(30)),
        Column('市净率', String(30)),
        Column('是否ST股', String(30))
    )
    UNIQUE_KEY = ['证券代码', '交易所行情日期']


class HistoryKDataPlusHour(Data):
    """历史A股K线数据_小时线"""
    TABLE_NAME = "K线_分钟_60"
    COLUMN_MAPPING = {
        'date': '交易所行情时间',
        'code': '证券代码',
        'open': '开盘价格',
        'high': '最高价',
        'low': '最低价',
        'close': '收盘价',
        'volume': '成交数量',
        'amount': '成交金额',
        'adjustflag': '复权状态'
    }
    METADATA = MetaData()
    TABLE_MATEDATA = Table(
        TABLE_NAME,
        METADATA,
        Column('交易所行情时间', Date, primary_key=True),
        Column('证券代码', String(30), primary_key=True),
        Column('开盘价格', String(30)),
        Column('最高价', String(30)),
        Column('最低价', String(30)),
        Column('收盘价', String(30)),
        Column('成交数量', String(30)),
        Column('成交金额', String(30)),
        Column('复权状态', String(30))
    )
    UNIQUE_KEY = ['证券代码', '交易所行情时间']


class HistoryKDataPlus30Min(Data):
    """历史A股K线数据_半小时线"""
    TABLE_NAME = "K线_分钟_30"
    COLUMN_MAPPING = {
        'date': '交易所行情时间',
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
    METADATA = MetaData()
    TABLE_MATEDATA = Table(
        TABLE_NAME,
        METADATA,
        Column('交易所行情时间', Date, primary_key=True),
        Column('证券代码', String(30), primary_key=True),
        Column('开盘价格', String(30)),
        Column('最高价', String(30)),
        Column('最低价', String(30)),
        Column('收盘价', String(30)),
        Column('成交数量', String(30)),
        Column('成交金额', String(30)),
        Column('复权状态', String(30))
    )
    UNIQUE_KEY = ['证券代码', '交易所行情时间']


class HistoryKDataPlus15Min(Data):
    """历史A股K线数据_15分钟线"""
    TABLE_NAME = "K线_分钟_15"
    COLUMN_MAPPING = {
        'date': '交易所行情时间',
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
    METADATA = MetaData()
    TABLE_MATEDATA = Table(
        TABLE_NAME,
        METADATA,
        Column('交易所行情时间', Date, primary_key=True),
        Column('证券代码', String(30), primary_key=True),
        Column('开盘价格', String(30)),
        Column('最高价', String(30)),
        Column('最低价', String(30)),
        Column('收盘价', String(30)),
        Column('成交数量', String(30)),
        Column('成交金额', String(30)),
        Column('复权状态', String(30))
    )
    UNIQUE_KEY = ['证券代码', '交易所行情时间']


class HistoryKDataPlus5Min(Data):
    """历史A股K线数据_分钟线"""
    TABLE_NAME = "K线_分钟_5"
    COLUMN_MAPPING = {
        'date': '交易所行情时间',
        'code': '证券代码',
        'open': '开盘价格',
        'high': '最高价',
        'low': '最低价',
        'close': '收盘价',
        'volume': '成交数量',
        'amount': '成交金额',
        'adjustflag': '复权状态'
    }
    METADATA = MetaData()
    TABLE_MATEDATA = Table(
        TABLE_NAME,
        METADATA,
        Column('交易所行情时间', Date, primary_key=True),
        Column('证券代码', String(30), primary_key=True),
        Column('开盘价格', String(30)),
        Column('最高价', String(30)),
        Column('最低价', String(30)),
        Column('收盘价', String(30)),
        Column('成交数量', String(30)),
        Column('成交金额', String(30)),
        Column('复权状态', String(30))
    )
    UNIQUE_KEY = ['证券代码', '交易所行情时间']


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
    METADATA = MetaData()
    TABLE_MATEDATA = Table(
        TABLE_NAME,
        METADATA,
        Column('证券代码', String(30), primary_key=True),
        Column('除权除息日期', Date, primary_key=True),
        Column('预披露公告日', Date),
        Column('股东大会公告日期', Date),
        Column('预案公告日', Date),
        Column('分红实施公告日', Date),
        Column('股权登记日', Date),
        Column('派息日', Date),
        Column('红股上市交易日', Date),
        Column('每股股利税前', String(30)),
        Column('每股股利税后', String(50)),
        Column('每股红股', String(30)),
        Column('分红送转', String(255)),
        Column('每股转增资本', String(30))
    )
    UNIQUE_KEY = ['证券代码', '除权除息日期']


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
    METADATA = MetaData()
    TABLE_MATEDATA = Table(
        TABLE_NAME,
        METADATA,
        Column('证券代码', String(30), primary_key=True),
        Column('除权除息日期', Date, primary_key=True),
        Column('向前复权因子', String(30)),
        Column('向后复权因子', String(30)),
        Column('本次复权因子', String(30))
    )
    UNIQUE_KEY = ['证券代码', '除权除息日期']


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
    METADATA = MetaData()
    TABLE_MATEDATA = Table(
        TABLE_NAME,
        METADATA,
        Column('证券代码', String(30), primary_key=True),
        Column('年', Integer, primary_key=True),
        Column('季度', Integer, primary_key=True),
        Column('财报发布日期', Date),
        Column('财报统计日期', Date),
        Column('净资产收益率平均', String(30)),
        Column('销售净利率', String(30)),
        Column('销售毛利率', String(30)),
        Column('净利润', String(30)),
        Column('每股收益', String(30)),
        Column('主营营业收入', String(30)),
        Column('总股本', String(30)),
        Column('流通股本', String(30))
    )
    UNIQUE_KEY = ['证券代码', '年', '季度']


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
    METADATA = MetaData()
    TABLE_MATEDATA = Table(
        TABLE_NAME,
        METADATA,
        Column('证券代码', String(30), primary_key=True),
        Column('年', Integer, primary_key=True),
        Column('季度', Integer, primary_key=True),
        Column('财报发布日期', Date),
        Column('财报统计日期', Date),
        Column('应收账款周转率', String(30)),
        Column('应收账款周转天数', String(30)),
        Column('存货周转率', String(30)),
        Column('存货周转天数', String(30)),
        Column('流动资产周转率', String(30)),
        Column('总资产周转率', String(30))
    )
    UNIQUE_KEY = ['证券代码', '年', '季度']


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
    METADATA = MetaData()
    TABLE_MATEDATA = Table(
        TABLE_NAME,
        METADATA,
        Column('证券代码', String(30), primary_key=True),
        Column('年', Integer, primary_key=True),
        Column('季度', Integer, primary_key=True),
        Column('财报发布日期', Date),
        Column('财报统计日期', Date),
        Column('净资产同比增长率', String(30)),
        Column('总资产同比增长率', String(30)),
        Column('净利润同比增长率', String(30)),
        Column('基本每股收益同比增长率', String(30)),
        Column('归属母公司股东净利润同比增长率', String(30))
    )
    UNIQUE_KEY = ['证券代码', '年', '季度']


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
    METADATA = MetaData()
    TABLE_MATEDATA = Table(
        TABLE_NAME,
        METADATA,
        Column('证券代码', String(30), primary_key=True),
        Column('年', Integer, primary_key=True),
        Column('季度', Integer, primary_key=True),
        Column('财报发布日期', Date),
        Column('财报统计日期', Date),
        Column('流动比率', String(30)),
        Column('速动比率', String(30)),
        Column('现金比率', String(30)),
        Column('总负债同比增长率', String(30)),
        Column('资产负债率', String(30)),
        Column('权益乘数', String(30))
    )
    UNIQUE_KEY = ['证券代码', '年', '季度']


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
    METADATA = MetaData()
    TABLE_MATEDATA = Table(
        TABLE_NAME,
        METADATA,
        Column('证券代码', String(30), primary_key=True),
        Column('年', Integer, primary_key=True),
        Column('季度', Integer, primary_key=True),
        Column('财报发布日期', Date),
        Column('财报统计日期', Date),
        Column('流动资产除以总资产', String(30)),
        Column('非流动资产除以总资产', String(30)),
        Column('有形资产除以总资产', String(30)),
        Column('已获利息倍数', String(30)),
        Column('经营活动现金流量净额除以营业收入', String(30)),
        Column('经营性现金净流量除以净利润', String(30)),
        Column('经营性现金净流量除以营业总收入', String(30))
    )
    UNIQUE_KEY = ['证券代码', '年', '季度']


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
    METADATA = MetaData()
    TABLE_MATEDATA = Table(
        TABLE_NAME,
        METADATA,
        Column('证券代码', String(30), primary_key=True),
        Column('年', Integer, primary_key=True),
        Column('季度', Integer, primary_key=True),
        Column('财报发布日期', Date),
        Column('财报统计日期', Date),
        Column('净资产收益率', String(30)),
        Column('权益乘数', String(30)),
        Column('总资产周转率', String(30)),
        Column('归属母公司净利润占比', String(30)),
        Column('净利润除以营业总收入', String(30)),
        Column('净利润除以利润总额', String(30)),
        Column('利润总额除以息税前利润', String(30)),
        Column('息税前利润除以营业总收入', String(30))
    )
    UNIQUE_KEY = ['证券代码', '年', '季度']


# ==================== 8 查询季频公司报告信息 ====================

class PerformanceExpressReport(Data):
    """季频公司业绩快报"""
    TABLE_NAME = "季频业绩快报"
    COLUMN_MAPPING = {
        'code': '证券代码',
        'performanceExpPubDate': '披露日',
        'performanceExpStatDate': '统计日期',
        'performanceExpUpdateDate': '更新日期',
        'performanceExpressTotalAsset': '总资产',
        'performanceExpressNetAsset': '净资产',
        'performanceExpressEPSChgPct': '业绩每股收益增长率',
        'performanceExpressROEWa': '净资产收益率加权',
        'performanceExpressEPSDiluted': '每股收益摊薄',
        'performanceExpressGRYOY': '营业总收入同比',
        'performanceExpressOPYOY': '营业利润同比'
    }
    METADATA = MetaData()
    TABLE_MATEDATA = Table(
        TABLE_NAME,
        METADATA,
        Column('证券代码', String(30), primary_key=True),
        Column('统计日期', Date, primary_key=True),
        Column('披露日', Date),
        Column('更新日期', Date),
        Column('总资产', String(30)),
        Column('净资产', String(30)),
        Column('业绩每股收益增长率', String(30)),
        Column('净资产收益率加权', String(30)),
        Column('每股收益摊薄', String(30)),
        Column('营业总收入同比', String(30)),
        Column('营业利润同比', String(30))
    )
    UNIQUE_KEY = ['证券代码', '统计日期']


class ForecastReport(Data):
    """季频公司业绩预告"""
    TABLE_NAME = "季频业绩预告"
    COLUMN_MAPPING = {
        'code': '证券代码',
        'profitForcastExpPubDate': '发布日期',
        'profitForcastExpStatDate': '统计日期',
        'profitForcastType': '类型',
        'profitForcastAbstract': '摘要',
        'profitForcastChgPctUp': '预告净利润增长上限',
        'profitForcastChgPctDwn': '预告净利润增长下限'
    }
    METADATA = MetaData()
    TABLE_MATEDATA = Table(
        TABLE_NAME,
        METADATA,
        Column('证券代码', String(30), primary_key=True),
        Column('统计日期', Date, primary_key=True),
        Column('发布日期', Date),
        Column('类型', String(50)),
        Column('摘要', String(200)),
        Column('预告净利润增长上限', String(30)),
        Column('预告净利润增长下限', String(30))
    )
    UNIQUE_KEY = ['证券代码', '统计日期']


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
    METADATA = MetaData()
    TABLE_MATEDATA = Table(
        TABLE_NAME,
        METADATA,
        Column('证券代码', String(30), primary_key=True),
        Column('证券名称', String(30)),
        Column('上市日期', Date),
        Column('退市日期', Date),
        Column('证券类型', String(30)),
        Column('上市状态', String(30))
    )
    UNIQUE_KEY = ['证券代码']

    @classmethod
    def transform(cls, df):
        df['上市日期'] = pd.to_datetime(df['上市日期'], errors='coerce')
        df['退市日期'] = pd.to_datetime(df['退市日期'], errors='coerce')
        type_map = {'1': '股票', '2': '指数', '3': '其它', '4': '可转债', '5': 'ETF'}
        df['证券类型'] = df['证券类型'].apply(lambda x: type_map.get(x, ''))
        status_map = {'1': '上市', '0': '退市'}
        df['上市状态'] = df['上市状态'].apply(lambda x: status_map.get(x, ''))
        return df


# ==================== 10 获取证券元信息 ====================

class TradeDates(Data):
    """交易日查询"""
    TABLE_NAME = "交易日历"
    COLUMN_MAPPING = {
        'calendar_date': '交易日期',
        'is_trading_day': '是否交易日'
    }
    METADATA = MetaData()
    TABLE_MATEDATA = Table(
        TABLE_NAME,
        METADATA,
        Column('交易日期', Date, primary_key=True),
        Column('是否交易日', Boolean)
    )
    UNIQUE_KEY = ['交易日期']

    @classmethod
    def transform(cls, df):
        bool_map = {'0': False, '1': True}
        df['是否交易日'] = df['是否交易日'].apply(lambda x: bool_map.get(x, None))
        return df


class AllStock(Data):
    """证券代码查询（全部证券列表）"""
    TABLE_NAME = "证券代码列表"
    COLUMN_MAPPING = {
        'code': '证券代码',
        'code_name': '证券名称',
        'tradeStatus': '交易状态'
    }
    METADATA = MetaData()
    TABLE_MATEDATA = Table(
        TABLE_NAME,
        METADATA,
        Column('日期', Date, primary_key=True),
        Column('证券代码', String(30), primary_key=True),
        Column('证券名称', String(30)),
        Column('交易状态', Boolean)
    )
    UNIQUE_KEY = ['日期', '证券代码']

    @classmethod
    def transform(cls, df):
        bool_map = {'0': False, '1': True}
        df['交易状态'] = df['交易状态'].apply(lambda x: bool_map.get(x, None))
        return df


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
    METADATA = MetaData()
    TABLE_MATEDATA = Table(
        TABLE_NAME,
        METADATA,
        Column('发布日期', Date, primary_key=True),
        Column('活期存款', String(30)),
        Column('定期存款三个月', String(30)),
        Column('定期存款半年', String(30)),
        Column('定期存款一年', String(30)),
        Column('定期存款二年', String(30)),
        Column('定期存款三年', String(30)),
        Column('定期存款五年', String(30)),
        Column('零存整取一年', String(30)),
        Column('零存整取三年', String(30)),
        Column('零存整取五年', String(30))
    )
    UNIQUE_KEY = ['发布日期']


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
    METADATA = MetaData()
    TABLE_MATEDATA = Table(
        TABLE_NAME,
        METADATA,
        Column('发布日期', Date, primary_key=True),
        Column('六个月贷款利率', String(30)),
        Column('六个月至一年贷款利率', String(30)),
        Column('一年至三年贷款利率', String(30)),
        Column('三年至五年贷款利率', String(30)),
        Column('五年以上贷款利率', String(30)),
        Column('五年以下公积金贷款利率', String(30)),
        Column('五年以上公积金贷款利率', String(30))
    )
    UNIQUE_KEY = ['发布日期']


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
    METADATA = MetaData()
    TABLE_MATEDATA = Table(
        TABLE_NAME,
        METADATA,
        Column('公告日期', Date, primary_key=True),
        Column('生效日期', Date),
        Column('大型金融机构调整前', String(30)),
        Column('大型金融机构调整后', String(30)),
        Column('中小型金融机构调整前', String(30)),
        Column('中小型金融机构调整后', String(30))
    )
    UNIQUE_KEY = ['公告日期']


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
    METADATA = MetaData()
    TABLE_MATEDATA = Table(
        TABLE_NAME,
        METADATA,
        Column('统计年度', String(30), primary_key=True),
        Column('统计月份', String(30), primary_key=True),
        Column('货币供应量M0', String(30)),
        Column('货币供应量M0同比', String(30)),
        Column('货币供应量M0环比', String(30)),
        Column('货币供应量M1', String(30)),
        Column('货币供应量M1同比', String(30)),
        Column('货币供应量M1环比', String(30)),
        Column('货币供应量M2', String(30)),
        Column('货币供应量M2同比', String(30)),
        Column('货币供应量M2环比', String(30))
    )
    UNIQUE_KEY = ['统计年度', '统计月份']


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
    METADATA = MetaData()
    TABLE_MATEDATA = Table(
        TABLE_NAME,
        METADATA,
        Column('统计年度', String(30), primary_key=True),
        Column('年货币供应量M0', String(30)),
        Column('年货币供应量M0同比', String(30)),
        Column('年货币供应量M1', String(30)),
        Column('年货币供应量M1同比', String(30)),
        Column('年货币供应量M2', String(30)),
        Column('年货币供应量M2同比', String(30))
    )
    UNIQUE_KEY = ['统计年度']


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
    METADATA = MetaData()
    TABLE_MATEDATA = Table(
        TABLE_NAME,
        METADATA,
        Column('证券代码', String(30), primary_key=True),
        Column('证券名称', String(30)),
        Column('所属行业', String(30)),
        Column('所属行业类别', String(30)),
        Column('更新日期', Date)
    )
    UNIQUE_KEY = ['证券代码']


class Sz50Stocks(Data):
    """上证50成分股"""
    TABLE_NAME = "成分股_上证50"
    COLUMN_MAPPING = {
        'code': '证券代码',
        'code_name': '证券名称',
        'updateDate': '更新日期'
    }
    METADATA = MetaData()
    TABLE_MATEDATA = Table(
        TABLE_NAME,
        METADATA,
        Column('证券代码', String(30), primary_key=True),
        Column('证券名称', String(30)),
        Column('更新日期', Date)
    )
    UNIQUE_KEY = ['证券代码']


class Hs300Stocks(Data):
    """沪深300成分股"""
    TABLE_NAME = "成分股_沪深300"
    COLUMN_MAPPING = {
        'code': '证券代码',
        'code_name': '证券名称',
        'updateDate': '更新日期'
    }
    METADATA = MetaData()
    TABLE_MATEDATA = Table(
        TABLE_NAME,
        METADATA,
        Column('证券代码', String(30), primary_key=True),
        Column('证券名称', String(30)),
        Column('更新日期', Date)
    )
    UNIQUE_KEY = ['证券代码']


class Zz500Stocks(Data):
    """中证500成分股"""
    TABLE_NAME = "成分股_中证500"
    COLUMN_MAPPING = {
        'code': '证券代码',
        'code_name': '证券名称',
        'updateDate': '更新日期'
    }
    METADATA = MetaData()
    TABLE_MATEDATA = Table(
        TABLE_NAME,
        METADATA,
        Column('证券代码', String(30), primary_key=True),
        Column('证券名称', String(50)),
        Column('更新日期', Date)
    )
    UNIQUE_KEY = ['证券代码']
