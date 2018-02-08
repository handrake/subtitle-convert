# subtitle-convert [![Build Status](https://travis-ci.org/handrake/subtitle-convert.svg?branch=master)](https://travis-ci.org/handrake/subtitle-convert)
자막 변환 프로그램

현재 SMI, SRT -> SMI, SRT, TXT 변환이 가능합니다. 인코딩도 지정이 가능합니다.

# 설치

## 실행 파일
zip 파일을 받고 압축을 푼 후 subtitle_convert.exe를 실행합니다.

## 소스 코드
```
git clone https://github.com/handrake/subtitle-convert.git
```
으로 소스를 다운받고

```
pip install -r requirements.txt
```

를 통해 의존 라이브러리를 설치합니다.

# 실행

```
python -m subtitle_convert
```

# 빌드

```
pyinstaller subtitle_convert.spec --clean -y
```

<img src="https://i.imgur.com/nIUM5UO.png" width="400">
