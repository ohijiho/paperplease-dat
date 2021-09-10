# paperplease-dat
동무, 려권내라우
### dattotar.py
```
./dattotar.py Art.dat.dec Art.tar
```
복호화된 paperplease 아카이브 파일을 tar파일로 변환
### tartodat.py
```
./tartodat.py Art.tar Art.dat.dec
```
tar 파일을 복호화된 paperplease 아카이브 파일로 변환
### PPTools.exe
http://games-gen.com/soft/PPTools.exe
### 동무, 려권내라우 고치기
[동무, 려권내라우](https://gall.dcinside.com/board/view/?id=game1&no=2614072)

PPTools.exe로 PapersPlease의 assets/Art.dat파일과 려권_문화어1.21-fixed개성.zip의 assets/Art.dat을 복호화하고, 두 파일을 dattotar.py로 변환한다.
  
PapersPlease에서 나온 tar파일의 내용물에 려권_문화어에서 나온 tar파일의 내용물을 덮어써서 하나의 tar파일로 합친다.
  
합친 tar파일을 tartodat.py로 변환하고, PPTools.exe로 암호화한 후 PapersPlease의 assets/Art.dat에 덮어쓴다.
