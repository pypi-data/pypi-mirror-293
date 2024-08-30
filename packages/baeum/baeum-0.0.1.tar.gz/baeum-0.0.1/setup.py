from setuptools import setup, find_packages

setup(
    name="baeum",  # 패키지 이름
    version="0.0.1",  # 버전
    packages=find_packages(),  # 포함할 패키지
    install_requires=[],  # 종속 패키지 목록
    author="baeum",  # 작성자 이름
    author_email="contact@baeum.io",  # 작성자 이메일
    description="",  # 패키지 설명
    long_description=open('README.md').read(),  # 패키지에 대한 자세한 설명
    long_description_content_type='text/markdown',  # 긴 설명의 형식
    url="https://git.baeum.io/baeum/pypi-baeum",  # 패키지의 URL
    classifiers=[  # 패키지 분류
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
