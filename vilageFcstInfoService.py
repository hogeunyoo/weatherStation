import serviceKey
import json, datetime,pytz

from customType import CodeValue, VilageFcstInfoService
from urllib.request import urlopen, Request
from urllib.parse import quote_plus, urlencode
    
class RequestParameter:
    def __init__(self,serviceKey,pageNo,numOfRows,dataType,base_date,base_time,nx,ny):
        self.serviceKey = serviceKey  # serviceKey.key
        self.pageNo = pageNo          # 1
        self.numOfRows = numOfRows    # 10
        self.dataType = dataType      # 'JSON'
        self.base_date = base_date    # 'YYYYmmdd'
        self.base_time = base_time    # 'HHMM'
        self.nx = nx                  # 61
        self.ny = ny                  # 121

class VilageFcstInfoServiceDatas(RequestParameter):
    def __init__(self,serviceKey,pageNo,numOfRows,dataType,base_date,base_time,nx,ny,getAPI):
        def request(getAPI):
            url = 'http://apis.data.go.kr/1360000/VilageFcstInfoService/' + getAPI.value 
            queryParams = '?' + 'serviceKey=' + serviceKey  + '&' + urlencode({ 
                    quote_plus('pageNo') : pageNo,
                    quote_plus('numOfRows') : numOfRows,
                    quote_plus('dataType') : dataType,
                    quote_plus('base_date') : base_date,
                    quote_plus('base_time') : base_time,
                    quote_plus('nx') : nx,
                    quote_plus('ny') : ny
                })
            request = Request(url + queryParams)
            request.get_method = lambda: 'GET' # 체크해
            response_body = urlopen(request).read()
            return response_body

        def get_service_status():
            status: bool = None
            if self.json_datas['response']['header']['resultCode'] == '00':
                status = True
            elif self.json_datas['response']['header']['resultCode'] is not None:
                status = False
            else:
                status = None
            return status

        super().__init__(serviceKey,pageNo,numOfRows,dataType,base_date,base_time,nx,ny)
        self.json_datas: dict = json.loads(request(getAPI))
        self.is_normal_service = get_service_status()

    def get_error_message(self):
        if self.is_normal_service is not None:
            print('Error Code: '+ self.json_datas['response']['header']['resultCode'] + '\nError Message: ' + self.json_datas['response']['header']['resultMsg'])
        else:
            print('알 수 없는 에러__001')

class VilageFcstInfoServices(VilageFcstInfoServiceDatas):
    __today = datetime.datetime.now(tz=pytz.timezone('Asia/Seoul')).strftime('%Y%m%d')
    __now = datetime.datetime.now(tz=pytz.timezone('Asia/Seoul')).strftime('%H%M')
    def __init__(self,serviceKey,nx,ny,getAPI,codeValue,pageNo=1,numOfRows=10,dataType='JSON',base_date=__today,base_time=__now):
        def get_std_date(date_now: str = base_date, time_now : str = base_time) : # 표준시간 생성함수
                standard_time = [2, 5, 8, 11, 14, 17, 20, 23]
                check_time = (int(time_now) // 100)
                day_calibrate = 0
                while not check_time in standard_time :
                    check_time -= 1
                    if check_time < 2 :
                        day_calibrate = 1
                        check_time = 23
                check_date = int(date_now) - day_calibrate
                check_time = '{:%H%M}'.format(datetime.time(check_time))
                
                print(check_date)
                return (str(check_date), check_time) #자릿수 문제
        def response_api(json_datas):
            response_data = None
            if self.is_normal_service == True:
                if getAPI == VilageFcstInfoService.GetVilageFcst: # 동네예보조회
                    for data in json_datas['response']['body']['items']['item'] :
                        if data['category'] == codeValue.value:
                            print('fcstValue : ' + data['fcstValue'])
                            response_data = data['fcstValue']
                elif getAPI == VilageFcstInfoService.GetUltraSrtFcst or getAPI == VilageFcstInfoService.GetUltraSrtNcst: # 초단기실황조회 or 초단기예보조회
                    for data in json_datas['response']['body']['items']['item'] :
                        if data['category'] == codeValue.value:
                            print('obsrValue : ' + data['obsrValue'])
                            response_data = data['obsrValue']
            elif self.is_normal_service == False:
                print(self.get_error_message())
            else:
                print('Error : 알 수 없는 에러_002')
            return response_data
        if getAPI == VilageFcstInfoService.GetUltraSrtFcst or getAPI == VilageFcstInfoService.GetUltraSrtNcst:
            super().__init__(serviceKey,pageNo,numOfRows,dataType,base_date,base_time,nx,ny,getAPI)
        elif getAPI == VilageFcstInfoService.GetVilageFcst :
            std_date, std_time = get_std_date(base_date, base_time)
            print('표준변환:', std_date, std_time)
            super().__init__(serviceKey,pageNo,numOfRows,dataType,std_date,std_time,nx,ny,getAPI)
        else:
            print('Error : getAPI 값 오류')
            super().__init__(serviceKey,pageNo,numOfRows,dataType,base_date,base_time,nx,ny,getAPI)
        self.result = response_api(self.json_datas)
        

        
# 작동 확인 테스트 코드
result = VilageFcstInfoServices(serviceKey=serviceKey.key,nx=61,ny=127,getAPI=VilageFcstInfoService.GetVilageFcst,codeValue=CodeValue.SKY).result
print(result)
