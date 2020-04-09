from enum import Enum

class CodeValue(Enum) :
    POP = 'POP' # 강수확률
    PTY = 'PTY' # 강수형태
    RN1 = 'RN1' # 1시간 강수량
    R06 = 'R06' # 6시간 강수량
    REH = 'REH' # 습도
    S06 = 'S06' # 6시간 신적설
    SKY = 'SKY' # 하늘상태
    T1H = 'T1G' # 기온
    T3H = 'T3H' # 3시간 기온
    TMN = 'TMN' # 아침 최저기온
    TMX = 'TMX' # 낮 최고기온
    UUU = 'UUU' # 풍속(동서성분)
    VVV = 'VVV' # 풍속(남북성분)
    WAV = 'WAV' # 파고
    VEC = 'VEC' # 풍향
    WSD = 'WSD' # 풍속

class VilageFcstInfoService(Enum) :
   GetUltraSrtNcst = 'getUltraSrtNcst' # 초단기실황조회
   GetUltraSrtFcst = 'getUltraSrtFcst' # 초단기예보조회
   GetVilageFcst = 'getVilageFcst' # 동네예보조회
#    GetFcstVersion = 'getFcstVersion' # 예보버전조회