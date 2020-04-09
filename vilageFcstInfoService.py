import serviceKey
import json
import pytz, datetime
from customType import CodeValue, VilageFcstInfoService

from urllib.request import urlopen, Request
from urllib.parse import quote_plus, urlencode

def vilageFcstInfoService( # None 타입 반환 가능함. 타입체크 바람. -> if vilageFcstInfoService() is None: 
    getAPI: VilageFcstInfoService,
    codeValue: CodeValue,
    base_date: str,
    base_time: str,
    nx: int,
    ny: int,
    pageNo: int = 1,
    numOfRows: int = 10,
    dataType: str = 'JSON'
    ):
    def jsonLoads(baseDate = base_date, baseTime = base_time):
        url = 'http://apis.data.go.kr/1360000/VilageFcstInfoService/' + getAPI.value 
        queryParams = '?' + 'serviceKey=' + serviceKey.key  + '&' + urlencode({ 
                quote_plus('pageNo') : pageNo,
                quote_plus('numOfRows') : numOfRows,
                quote_plus('dataType') : dataType,
                quote_plus('base_date') : baseDate,
                quote_plus('base_time') : baseTime,
                quote_plus('nx') : nx,
                quote_plus('ny') : ny
            })
        request = Request(url + queryParams)
        request.get_method = lambda: 'GET' # 체크해
        response_body = urlopen(request).read()
        jsonDatas = json.loads(response_body)
        return jsonDatas
    
    jsonDatas = jsonLoads() # json 데이터를 딕셔너리로 치환함

    def response_api(jsonDatas = jsonDatas):
        print(jsonDatas['response']['header']['resultMsg'])
        if getAPI == VilageFcstInfoService.GetVilageFcst : # 동네예보조회
            for data in jsonDatas['response']['body']['items']['item'] :
                if data['category'] == codeValue.value:
                    print('fcstValue : ' + data['fcstValue'])
                    return data['fcstValue']
        # elif getAPI == VilageFcstInfoService.GetFcstVersion : # 예보버전조회 코드
        #     print('미구현')
        else : # 초단기실황조회 or 초단기예보조회
            for data in jsonDatas['response']['body']['items']['item'] :
                if data['category'] == codeValue.value:
                    print('obsrValue : ' + data['obsrValue'])
                    return data['obsrValue']

    if jsonDatas['response']['header']['resultCode'] == '00':
        return response_api()
    elif jsonDatas['response']['header']['resultCode'] == '99': # 현재 시간대에 발표된 자료가 없을 때
        def get_std_date() : # 표준시간 생성함수
            standard_time = [2, 5, 8, 11, 14, 17, 20, 23]
            time_now = datetime.datetime.now(tz=pytz.timezone('Asia/Seoul')).strftime('%H')
            check_time = int(time_now) - 1
            day_calibrate = 0
            while not check_time in standard_time :
                check_time -= 1
                if check_time < 2 :
                    day_calibrate = 1
                    check_time = 23
            date_now = datetime.datetime.now(tz=pytz.timezone('Asia/Seoul')).strftime('%Y%m%d')
            check_date = int(date_now) - day_calibrate
            return (str(check_date), (str(check_time) + '00'))
        std_date, std_time = get_std_date()
        jsonLoads(baseDate = std_date,baseTime = std_time)
        return response_api(jsonDatas=jsonLoads(baseDate = std_date,baseTime = std_time))
    else: # Error
        if jsonDatas['response']['header']['resultMsg'] is None:
            print('알 수 없는 에러')
        else: 
            print('Error Code: '+ jsonDatas['response']['header']['resultCode'] + '\nError Message: ' + jsonDatas['response']['header']['resultMsg'])



## 작동 확인 테스트 코드
# today = datetime.datetime.now(tz=pytz.timezone('Asia/Seoul')).strftime('%Y%m%d')
# now = datetime.datetime.now(tz=pytz.timezone('Asia/Seoul')).strftime('%H%M')
# print(vilageFcstInfoService(getAPI = VilageFcstInfoService.GetVilageFcst, codeValue = CodeValue.SKY, base_date = today, base_time = now, nx = 61,ny = 127)) #61,127 고려대

