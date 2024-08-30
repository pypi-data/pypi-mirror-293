from setuptools import find_packages, setup

setup(
    name="otsuwinhdlr",
    version="1.0.5.311",
    url="https://github.com/Otsuhachi/OtsuWinHdlr",
    description="ウィンドウやエクスプローラのハンドル取得、操作を補助します。",
    author="Otsuhachi",
    author_email="agequodagis.tufuiegoeris@gmail.com",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "otsutil",
        "otsuvalidator",
        "otsuwinAPI",
    ],
    python_requires=">=3.11",
)
