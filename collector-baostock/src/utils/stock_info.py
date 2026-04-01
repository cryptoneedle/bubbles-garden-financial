"""
证券信息查询工具模块
提供从数据库获取证券基本信息的功能
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

import pandas as pd
from sqlalchemy import text

from db.database import engine, schema


def get_all_stocks() -> pd.DataFrame:
    """
    获取所有证券基本信息

    Returns:
        pd.DataFrame: 包含证券代码、证券名称、上市日期等信息的DataFrame
    """
    with engine.connect() as conn:
        query = f"SELECT * FROM {schema}.证券基本资料"
        result = conn.execute(text(query))
        df = pd.DataFrame(result.fetchall(), columns=result.keys())
    return df


def get_stock_by_code(stock_code: str) -> pd.DataFrame:
    """
    根据证券代码查询证券信息

    Args:
        stock_code: 证券代码，如 "sh.600000"

    Returns:
        pd.DataFrame: 匹配的证券信息
    """
    with engine.connect() as conn:
        query = f'SELECT * FROM "{schema}"."证券基本资料" WHERE "证券代码" = :code'
        result = conn.execute(text(query), {"code": stock_code})
        df = pd.DataFrame(result.fetchall(), columns=result.keys())
    return df


def get_stocks_by_name(stock_name: str) -> pd.DataFrame:
    """
    根据证券名称模糊查询证券信息

    Args:
        stock_name: 证券名称，支持模糊匹配

    Returns:
        pd.DataFrame: 匹配的证券信息
    """
    with engine.connect() as conn:
        query = f'SELECT * FROM "{schema}"."证券基本资料" WHERE "证券名称" LIKE :name'
        result = conn.execute(text(query), {"name": f"%{stock_name}%"})
        df = pd.DataFrame(result.fetchall(), columns=result.keys())
    return df


def get_stocks_by_type(stock_type: str) -> pd.DataFrame:
    """
    根据证券类型查询证券信息

    Args:
        stock_type: 证券类型，如 "股票"、"指数"、"ETF" 等

    Returns:
        pd.DataFrame: 匹配的证券信息
    """
    with engine.connect() as conn:
        query = f'SELECT * FROM "{schema}"."证券基本资料" WHERE "证券类型" = :type'
        result = conn.execute(text(query), {"type": stock_type})
        df = pd.DataFrame(result.fetchall(), columns=result.keys())
    return df


def get_stock_industry(stock_code: str = None) -> pd.DataFrame:
    """
    获取行业分类信息

    Args:
        stock_code: 可选，指定证券代码查询特定证券的行业信息

    Returns:
        pd.DataFrame: 行业分类信息
    """
    with engine.connect() as conn:
        if stock_code:
            query = f'SELECT * FROM "{schema}"."行业分类" WHERE "证券代码" = :code'
            result = conn.execute(text(query), {"code": stock_code})
        else:
            query = f'SELECT * FROM "{schema}"."行业分类"'
            result = conn.execute(text(query))
        df = pd.DataFrame(result.fetchall(), columns=result.keys())
    return df


def get_index_stocks(index_name: str) -> pd.DataFrame:
    """
    获取指数成分股列表

    Args:
        index_name: 指数名称，支持 "上证50"、"沪深300"、"中证500"

    Returns:
        pd.DataFrame: 指数成分股列表
    """
    table_map = {
        "上证50": "成分股_上证50",
        "沪深300": "成分股_沪深300",
        "中证500": "成分股_中证500"
    }

    table_name = table_map.get(index_name)
    if not table_name:
        raise ValueError(f"不支持的指数名称: {index_name}，支持的指数: {list(table_map.keys())}")

    with engine.connect() as conn:
        query = f'SELECT * FROM "{schema}"."{table_name}"'
        result = conn.execute(text(query))
        df = pd.DataFrame(result.fetchall(), columns=result.keys())
    return df


if __name__ == '__main__':
    # 测试代码
    print("=" * 50)
    print("测试获取所有证券信息（前5条）:")
    print(get_all_stocks().head())

    print("\n" + "=" * 50)
    print("测试根据代码查询证券:")
    print(get_stock_by_code("sh.600000"))

    print("\n" + "=" * 50)
    print("测试根据名称模糊查询证券:")
    print(get_stocks_by_name("茅台"))

    print("\n" + "=" * 50)
    print("测试获取行业分类信息（前5条）:")
    print(get_stock_industry().head())

    print("\n" + "=" * 50)
    print("测试获取沪深300成分股（前5条）:")
    print(get_index_stocks("沪深300").head())
