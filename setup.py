from setuptools import setup

setup(
    name='movieRecommendation',
    version='1.0.0',
    long_description="recommend movie",
    packages=['movieRecommendation'],
    include_package_data=True,
    zip_safe=False,
    install_requires=['Flask', 'flask_sqlalchemy']
)