from setuptools import setup
 
setup(
    name='AppDT',
    version='1.0.0',
    description='(This Is A Chinese Package)此工具箱可以帮您快速构建Windows™应用程序，也可以快速生成安装包',
    author='xumouren225588',
    author_email='xumouren225588@163.com',
    url="https://www.douyin.com/user/MS4wLjABAAAARkk5zY-7-Et1347qxL_7rsHVzWHOh9NI1YbMAZZ8crI",
    packages=['AppDT'],
    license='MIT',
    install_requires=[
        'pyinstaller',
        'PyQt5'
    ],
    python_requires='>=3.5',
    entry_points={
        'console_scripts': [
            'adt=AppDT.whlcode:adt',
        ],
    },
    classifiers=[
        
        "Programming Language :: Python",
        "Operating System :: Microsoft :: Windows",
    ],
)
