import sys
from datetime import date, datetime, timedelta
from pathlib import Path

from dateutil.relativedelta import relativedelta
from pangres import engine
from sqlalchemy import text
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

    baostock.login()

    with engine.begin() as conn:
        conn.execute(text("DROP TABLE IF EXISTS baostock." + StockIndustry.TABLE_NAME))
    StockIndustry.METADATA.create_all(engine, checkfirst=True)
    with engine.begin() as conn:
        conn.execute(text("DROP TABLE IF EXISTS baostock." + Sz50Stocks.TABLE_NAME))
    Sz50Stocks.METADATA.create_all(engine, checkfirst=True)
    with engine.begin() as conn:
        conn.execute(text("DROP TABLE IF EXISTS baostock." + Hs300Stocks.TABLE_NAME))
    Hs300Stocks.METADATA.create_all(engine, checkfirst=True)
    with engine.begin() as conn:
        conn.execute(text("DROP TABLE IF EXISTS baostock." + Zz500Stocks.TABLE_NAME))
    Zz500Stocks.METADATA.create_all(engine, checkfirst=True)

    for date in tqdm(pd.date_range(start='1991-08-17', end='today', freq='D')):
        current_date = date.strftime('%Y-%m-%d')
        print(current_date)
        # 12.1 行业分类：query_stock_industry()
        StockIndustry.dealAndStorage(rs=baostock.query_stock_industry(date=current_date))
        # 12.2 上证50成分股：query_sz50_stocks()
        Sz50Stocks.dealAndStorage(rs=baostock.query_sz50_stocks(date=current_date))
        # 12.3 沪深300成分股：query_hs300_stocks()
        Hs300Stocks.dealAndStorage(rs=baostock.query_hs300_stocks(date=current_date))
        # 12.4 中证500成分股：query_zz500_stocks()
        Zz500Stocks.dealAndStorage(rs=baostock.query_zz500_stocks(date=current_date))

    baostock.logout()
