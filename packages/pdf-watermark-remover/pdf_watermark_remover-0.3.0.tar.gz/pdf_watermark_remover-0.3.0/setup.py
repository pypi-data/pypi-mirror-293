from setuptools import setup, find_packages

setup(
    name='pdf_watermark_remover',
    version='0.3.0',
    packages=find_packages(),
    install_requires=[
        'opencv-python-headless',
        'numpy',
        'Pillow',
        'PyMuPDF',
        'reportlab',
    ],
    entry_points={
        'console_scripts': [
            'pdf_watermark_remover=pdf_watermark_remover.remover:process_pdf',
        ],
    },
    author='huapohen',
    author_email='694450321@qq.com',
    description='A package to remove watermarks from PDF files',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/huapohen/pdf_watermark_remover',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
