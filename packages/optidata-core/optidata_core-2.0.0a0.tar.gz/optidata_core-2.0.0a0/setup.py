from setuptools import setup, find_packages

VERSION = '2.0.0a'  # settings.APP_VERSION
DESCRIPTION = 'Paquete de Python para OptiData'
LONG_DESCRIPTION = 'Paquete para OptiData que contiene funcionalidades para realizar una Conciliación con Pandas y Vaex'

# Configurando
setup(
    name="optidata-core",
    version=VERSION,
    author="Gonzalo Torres Moya",
    author_email="<gtorres@optimisa.cl>",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    packages=find_packages(where="app"),
    package_dir={"": "app"},
    keywords=['python', 'optidata-core'],
    license="MIT",
    install_requires=[
        "flask==3.0.3",
        "Flask-Bcrypt==1.0.1",
        "Flask-JWT-Extended==4.6.0",
        "Flask-Compress==1.15",
        "Flask-Cors==4.0.1",
        "flask-restx==1.3.0",
        "numpy==1.26.4",
        "openpyxl==3.1.5",
        "pandas==2.1.0",
        "pymongo==4.8.0",
        "pysftp==0.2.9",
        "vaex==4.17.0",
        "pydantic-settings==2.4.0",
        "kafka-python==2.0.2",
        "joblib==1.4.2",
        "paramiko==3.4.1",
        "oracledb==2.4.1",
        "SQLAlchemy==2.0.32",
        "APScheduler==3.10.4",
        "Fernet==1.0.1",
        "retrying==1.3.4",
        "pycryptodome==3.20.0",
        "cryptography==43.0.0",
        "werkzeug==3.0.4",
        "setuptools==73.0.1",
        "chardet==5.2.0",
        "bcrypt==4.2.0",
        "anyio==4.4.0",
        "pillow==10.4.0",
        "pydantic==2.8.2",
        "Paste==3.10.1",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.9"
)
