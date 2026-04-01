import os
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

# 加载 .env 文件
load_dotenv()

# 单例缓存
_engine = None
_schema = None

def get_engine():
    """获取数据库 Engine（单例模式）"""
    global _engine

    if _engine is None:
        # 1. 获取环境变量（这里提供了默认值以防报错，生产环境建议去掉默认值强制校验）
        db_user = os.getenv("DB_USERNAME", os.getenv("DB_USER", "postgres"))
        db_password = os.getenv("DB_PASSWORD", "123456")
        db_host = os.getenv("DB_HOST", "localhost")
        db_port = os.getenv("DB_PORT", "5432")
        db_name = os.getenv("DB_NAME", "postgres")
        db_schema = os.getenv("DB_SCHEMA", "public")

        # 2. 拼接 SQLAlchemy 数据库 URL
        # 推荐使用 psycopg2 驱动处理 pandas 的批量写入
        db_url = f"postgresql+psycopg2://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"

        # 3. 创建 Engine
        # pool_size: 连接池常驻连接数
        # max_overflow: 连接池满后可额外增加的连接数
        # pool_pre_ping: 每次从池中获取连接前，进行“ping”测试，防止使用了已断开的连接
        _engine = create_engine(
            db_url,
            pool_size=5,
            max_overflow=10,
            pool_pre_ping=True,
            # echo=True  # 如果需要打印 SQL 语句进行调试，可以取消注释
            connect_args={'options': f'-c search_path={db_schema}'}
        )

    return _engine

def get_schema():
    """获取数据库Schema"""
    global _schema
    return os.getenv("DB_SCHEMA", "public")

# 直接暴露 engine 对象供业务代码极简导入
engine = get_engine()
schema = get_schema()


def test_connection():
    """测试数据库连接是否正常"""
    try:
        with engine.connect() as conn:
            result = conn.execute(text("SELECT version()"))
            version = result.scalar()
            print(f"数据库连接成功！")
            print(f"PostgreSQL 版本: {version}")
            return True
    except Exception as e:
        print(f"数据库连接失败: {e}")
        return False


if __name__ == "__main__":
    test_connection()