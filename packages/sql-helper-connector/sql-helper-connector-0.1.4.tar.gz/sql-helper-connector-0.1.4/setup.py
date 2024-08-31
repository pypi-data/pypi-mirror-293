from setuptools import setup, find_packages
# 读取 README 文件作为长描述
with open("CONNECTOR_README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()


setup(
    name='sql-helper-connector',
    version='0.1.4',
    packages=find_packages(include=['connector', 'connector.*']),
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://www.clustro.ai/",
    description='clustroai_sql_helper',
    author='clustro ai',
    author_email='clustro@clustro.ai',
    include_package_data=True,
    install_requires=[
        'click',  # 确保列出了所有依赖
        'PyMySQL==1.1.0',
        'pg8000==1.30.5',
        'requests==2.31.0',
        'python-engineio==4.4.1',
        'python-socketio[client]==5.8.0'
    ],
    entry_points='''
        [console_scripts]
        sql_helper_connector=connector.sql_helper_connector:handle_connection
    ''',
)
