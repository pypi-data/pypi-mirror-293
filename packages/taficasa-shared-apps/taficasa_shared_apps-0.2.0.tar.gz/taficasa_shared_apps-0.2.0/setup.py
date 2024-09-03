from setuptools import setup, find_packages

setup(
    name="taficasa_shared_apps",
    version="0.2.0", 
    author="Excel Okechukwu",
    author_email="excel@taficasa.com",
    description="This package contains folders and apps needed within TafiCasa apps",
    long_description=open('README.rst').read(),
    long_description_content_type="text/x-rst",
    license="Custom License",  
    classifiers=[
        "Framework :: Django",
        "Programming Language :: Python :: 3",
    ],
    packages=find_packages(), 
    python_requires=">=3.8",
    install_requires=[
        "Django==4.2.2",
        'django-rest-knox==4.2.0',
        'djangorestframework==3.14.0',
        'google-cloud-tasks==2.16.3',
        'google-cloud-scheduler==2.13.3',
    ],
   
)
