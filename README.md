# subtitle-convert [![Build Status](https://travis-ci.org/handrake/subtitle-convert.svg?branch=master)](https://travis-ci.org/handrake/subtitle-convert)
자막 변환 프로그램

현재 SMI, SRT -> SMI, SRT, TXT 변환이 가능합니다. 인코딩도 지정이 가능합니다.

<img src="https://i.imgur.com/nIUM5UO.png" width="400">

# 설치

## 실행 파일
SubtitleConvertSetup.exe 파일을 실행해서 설치합니다.

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

## 실행 파일 생성

```
pyinstaller subtitle_convert.spec --clean -y
```

## 인스톨러 생성

* Inno Setup과 [Unofficial Korean 언어팩](https://github.com/jrsoftware/issrc/blob/master/Files/Languages/Unofficial/Korean.isl)이 필요합니다.

```
iscc subtitle_convert.iss
```

Output 폴더에 SubtitleConvertSetup.exe가 만들어집니다.
