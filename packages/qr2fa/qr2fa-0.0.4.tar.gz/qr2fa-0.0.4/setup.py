from setuptools import setup, find_packages

setup(
    name='qr2fa',
    version='0.0.4',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'qr2fa = qr2fa:main',
        ],
    },
    install_requires=[
        'opencv-python',
        'pyzbar',
        'pyotp',
        'argparse'
    ],
    author='NghiaHL',
    description='QR Code Decoder and OTP Generator.'
)