import sys
from pathlib import Path

import pandas as pd
from dateutil.relativedelta import relativedelta
from datetime import date

from tqdm import tqdm

sys.path.insert(0, str(Path(__file__).parent.parent))

import baostock
from base.data_define import *
from utils.stock_info import get_all_stocks, get_stock_by_code

if __name__ == '__main__':
    # === 计算日期 ===
    base_date = date.today()
    FMT_DAY = "%Y-%m-%d"
    FMT_MONTH = "%Y-%m"
    FMT_YEAR = "%Y"

    # === 1. 日 ===
    yesterday = (base_date - relativedelta(days=1)).strftime(FMT_DAY)
    today = base_date.strftime(FMT_DAY)
    tomorrow = (base_date + relativedelta(days=1)).strftime(FMT_DAY)
    print(f"{yesterday}\n{today}\n{tomorrow}")

    # === 2. 月 ===
    last_month = (base_date - relativedelta(months=1)).strftime(FMT_MONTH)
    month = base_date.strftime(FMT_MONTH)
    next_month = (base_date + relativedelta(months=1)).strftime(FMT_MONTH)
    print("\n--- 月 ---")
    print(f"{last_month}\n{month}\n{next_month}")

    # === 3. 年 ===
    last_year = (base_date - relativedelta(years=1)).strftime(FMT_YEAR)
    year = base_date.strftime(FMT_YEAR)
    next_year = (base_date + relativedelta(years=1)).strftime(FMT_YEAR)
    print("\n--- 年 ---")
    print(f"{last_year}\n{year}\n{next_year}")

    # === 4. 每年初 ===
    year_begin_day = date(base_date.year, 1, 1).strftime(FMT_DAY)
    next_year_begin_day = date(base_date.year + 1, 1, 1).strftime(FMT_DAY)
    print("\n--- 年初 ---")
    print(f"{year_begin_day}\n{next_year_begin_day}")

    rs = baostock.login()

    # ========== ✅ 9 证券基本资料 ==================
    # 9.1 证券基本资料：query_stock_basic()
    StockBasic.dealAndStorage(rs=baostock.query_stock_basic())

    # ========== ✅ 10 获取证券元信息 ===============
    # 10.1 交易日查询：query_trade_dates()
    # 时间范围：2017-2018年数据
    TradeDates.dealAndStorage(rs=baostock.query_trade_dates())
    # 10.2 证券代码查询：query_all_stock()
    # 时间范围：默认当天，闭市后日K线数据更新
    for date in tqdm(pd.date_range(start='1990-01-01', end='today', freq='D')):
        day = date.strftime('%Y-%m-%d')
        AllStock.dealAndStorage(rs=baostock.query_all_stock(day), date=day)

    # ========== ✅ 12 板块数据 ====================
    # 入库时间：每周一下午
    for date in tqdm(pd.date_range(start='1990-01-01', end='today', freq='D')):
        current_date = date.strftime('%Y-%m-%d')
        # 12.1 行业分类：query_stock_industry()
        StockIndustry.dealAndStorage(rs=baostock.query_stock_industry(date=current_date))
        # 12.2 上证50成分股：query_sz50_stocks()
        Sz50Stocks.dealAndStorage(rs=baostock.query_sz50_stocks(date=current_date))
        # 12.3 沪深300成分股：query_hs300_stocks()
        Hs300Stocks.dealAndStorage(rs=baostock.query_hs300_stocks(date=current_date))
        # 12.4 中证500成分股：query_zz500_stocks()
        Zz500Stocks.dealAndStorage(rs=baostock.query_zz500_stocks(date=current_date))

    stocks = get_all_stocks()

    # ========== 4 获取历史A股K线数据 =============
    # TODO 没有测分钟的
    HistoryKDataPlusMonth.dealAndStorage(rs=baostock.query_history_k_data_plus("sh.600000",
                                                                               "date,code,open,high,low,close,volume,amount,adjustflag,turn,pctChg",
                                                                               "1990-01-01", current_day_str, 'm'))
    HistoryKDataPlusWeek.dealAndStorage(rs=baostock.query_history_k_data_plus("sh.600000",
                                                                              "date,code,open,high,low,close,volume,amount,adjustflag,turn,pctChg",
                                                                              "1990-01-01", current_day_str, 'w'))
    HistoryKDataPlusDay.dealAndStorage(rs=baostock.query_history_k_data_plus("sh.600000",
                                                                             "date,code,open,high,low,close,preclose,volume,amount,adjustflag,turn,tradestatus,pctChg,isST",
                                                                             "1990-01-01", current_day_str, 'd'))
    # 4.1 获取历史A股K线数据：query_history_k_data_plus()
    # 月K线   入库时间：每月1号17:30  股票时间范围：1990-12-19至今 ETF时间范围：2026-01-05至今 指数：2006-01-01至今（综合指数，规模指数，一级行业指数，二级行业指数，策略指数，成长指数，价值指数，主题指数，基金指数，债券指数）
    # 周K线   入库时间：周六17:30    股票时间范围：1990-12-19至今 ETF时间范围：2026-01-05至今 指数：2006-01-01至今（综合指数，规模指数，一级行业指数，二级行业指数，策略指数，成长指数，价值指数，主题指数，基金指数，债券指数）
    # 日K线   入库时间：当前交易日17:30 股票时间范围：1990-12-19至今 ETF时间范围：2026-01-05至今 指数：2006-01-01至今（综合指数，规模指数，一级行业指数，二级行业指数，策略指数，成长指数，价值指数，主题指数，基金指数，债券指数）
    # 分钟K线  入库时间：当前交易日20:00 股票时间范围：2019-01-02至今（近5年） ETF时间范围：2026-01-05至今
    # 4.2 历史行情指标参数

    # ========== 5 查询除权除息信息 ===============
    # 5.1 除权除息信息：query_dividend_data()
    # 时间范围：1990至今
    for index, row in tqdm(get_all_stocks().iterrows()):
        code = row['证券代码']
        for year in range(1990, next_year):
            DividendData.dealAndStorage(rs=baostock.query_dividend_data(code=code, year=year), year=year)

    # ========== 6 查询复权因子信息 ===============
    # 入库时间：当前交易日18:00
    # 6.1 复权因子：query_adjust_factor()
    for index, row in get_all_stocks().iterrows():
        code = row['证券代码']
        AdjustFactor.dealAndStorage(rs=baostock.query_adjust_factor(code, '1990-01-01', current_day_str))

    # ========== 7 查询季频财务数据信息 ============
    # 入库时间：第二自然日1:30
    # 时间范围：2007年至今
    for index, row in get_all_stocks().iterrows():
        code = row['证券代码']
        for year in range(2007, current_year):
            for quarter in range(1, 5):
                # 7.1 季频盈利能力：query_profit_data()
                ProfitData.dealAndStorage(rs=baostock.query_profit_data(code, year, quarter), year=year,
                                          quarter=quarter)
                # 7.2 季频营运能力：query_operation_data()
                OperationData.dealAndStorage(rs=baostock.query_operation_data(code, year, quarter), year=year,
                                             quarter=quarter)
                # 7.3 季频成长能力：query_growth_data()
                GrowthData.dealAndStorage(rs=baostock.query_growth_data(code, year, quarter), year=year,
                                          quarter=quarter)
                # 7.4 季频偿债能力：query_balance_data()
                BalanceData.dealAndStorage(rs=baostock.query_balance_data(code, year, quarter), year=year,
                                           quarter=quarter)
                # 7.5 季频现金流量：query_cash_flow_data()
                CashFlowData.dealAndStorage(rs=baostock.query_cash_flow_data(code, year, quarter), year=year,
                                            quarter=quarter)
                # 7.6 季频杜邦指数：query_dupont_data()
                DupontData.dealAndStorage(rs=baostock.query_dupont_data(code, year, quarter), year=year,
                                          quarter=quarter)

    # ========== 8 查询季频公司报告信息 ===========
    # 入库时间：第二自然日1:30
    for index, row in get_all_stocks().iterrows():
        code = row['证券代码']
        # 8.1 季频公司业绩快报：query_performance_express_report()
        # 时间范围：2003年至今 或者 06
        PerformanceExpressReport.dealAndStorage(
            rs=baostock.query_performance_express_report(code, '1900-01-01', current_day))
        # 8.2 季频公司业绩预告：query_forecast_report()
        # 时间范围：2006年至今 或者 03
        ForecastReport.dealAndStorage(rs=baostock.query_forecast_report(code, '1900-01-01', current_day))

    # ========== 11 宏观经济数据 =================
    # 11.1 存款利率：query_deposit_rate_data()
    DepositRateData.dealAndStorage(rs=baostock.query_deposit_rate_data("1990-01-01", current_day_str))
    # 11.2 贷款利率：query_loan_rate_data()
    LoanRateData.dealAndStorage(rs=baostock.query_loan_rate_data("1990-01-01", current_day_str))
    # 11.3 存款准备金率：query_required_reserve_ratio_data()
    RequiredReserveRatioData.dealAndStorage(rs=baostock.query_required_reserve_ratio_data("1990-01", current_day_str))
    # 11.4 货币供应量：query_money_supply_data_month()
    MoneySupplyDataMonth.dealAndStorage(rs=baostock.query_money_supply_data_month("1990-01", current_month_str))
    # 11.5 货币供应量(年底余额)：query_money_supply_data_year()
    MoneySupplyDataYear.dealAndStorage(rs=baostock.query_money_supply_data_year("1990", current_year))

    rs = baostock.logout()
