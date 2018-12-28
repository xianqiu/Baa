from setuptools import setup


setup(
    name='baa',
    version=__import__('baa').__version__,
    description="Baa~ Baa~",
    author='qx3501332',
    author_email='x.qiu@qq.com',
    license="MIT License",
    url='https://github.com/xianqiu/Baa',
    packages=['baa'],
    package_data={'baa': ['mail_template']},
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.6",
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
    zip_safe=False,
)
