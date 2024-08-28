from analyser_hj3415.analysers import eval, score
from db_hj3415.myredis import Base
import json
from collections import OrderedDict
from db_hj3415 import myredis as db_myredis


page = '.analyser'


def red_ranking() -> OrderedDict:
    """
    redis를 사용하며 red score를 계산해서 0이상의 값을 가지는 종목을 순서대로 저장하여 반환한다.
    :return: OrderedDict([('023590', 101),
             ('009970', 99),
             ('010060', 91),...])
    """
    redis_name = 'red_ranking'

    try:
        cached_data = Base.redis_client.get(redis_name).decode('utf-8')
    except AttributeError:
        # redis에 해당하는 값이 없는 경우
        data = {}
        for i, code in enumerate(db_myredis.Corps.list_all_codes()):
            s = score.red(code)
            if s <= 0:
                continue
            data[code] = s
            # print(i, code, s)

        # print(data)
        if data:
            # 데이터를 Redis에 캐싱
            Base.redis_client.set(redis_name, json.dumps(data))
            # 12시간 후 키가 자동으로 제거됨
            Base.redis_client.expire(redis_name, 3600 * 12)
        print("analysers.eval 데이터 계산하기 - myredis.red_ranking")
        # ordereddict를 이용해서 딕셔너리의 값을 기준으로 내림차순 정렬함.
        return OrderedDict(sorted(data.items(), key=lambda item: item[1], reverse=True))
    else:
        print(f"Redis 캐시에서 데이터 가져오기(남은시간:{round(Base.redis_client.ttl(redis_name)/3600,1)}시간) - myredis.red_ranking")
        # ordereddict를 이용해서 딕셔너리의 값을 기준으로 내림차순 정렬함.
        return OrderedDict(sorted(json.loads(cached_data).items(), key=lambda item: item[1], reverse=True))





def red_n_score(code: str) -> dict:
    """
    redis 사용 - 소멸타이머 사용
    리턴값
    {
        'red_price': red_price,
        '사업가치': 사업가치,
        '재산가치': 재산가치,
        '부채평가': 부채평가,
        '발행주식수': 발행주식수,
        'date': [각 유효한 값의 년월값 리스트(ex- 2020/09)],
    }
    """
    redis_name = code + page + '_eval_' + 'red'
    try:
        cached_data = Base.redis_client.get(redis_name).decode('utf-8')
    except AttributeError:
        # redis에 해당하는 값이 없는 경우
        data = eval.red(code)
        data['score'] = score.red(code)
        # print(data)
        if data:
            # 데이터를 Redis에 캐싱
            Base.redis_client.set(redis_name, json.dumps(data))
            # 60분후 키가 자동으로 제거됨
            Base.redis_client.expire(redis_name, 3600)
        print("analysers.eval 데이터 계산하기 - myredis.red")
        return data
    else:
        print(f"Redis 캐시에서 데이터 가져오기(남은시간:{Base.redis_client.ttl(redis_name)}초) - myredis.red")
        return json.loads(cached_data)


def mil_n_score(code: str) -> dict:
    """
    redis 사용 - 소멸타이머 사용
    리턴값
    {
        '주주수익률': 주주수익률,
        '이익지표': 이익지표,
        '투자수익률': {'ROIC': roic, 'ROE': roe , 'ROE106': {}},
        '가치지표': {'FCF': fcf_dict, 'PFCF': pfcf_dict, 'PCR': pcr_dict},
        'date': [각 유효한 값의 년월값 리스트(ex- 2020/09)],
    }

    - 재무활동현금흐름이 마이너스라는 것은 배당급 지급했거나, 자사주 매입했거나, 부채를 상환한 상태임.
    - 반대는 채권자로 자금을 조달했거나 신주를 발행했다는 의미
    <주주수익률> - 재무활동현금흐름/시가총액 => 5%이상인가?

    투하자본수익률(ROIC)가 30%이상인가
    ROE(자기자본이익률) 20%이상이면 아주 우수 다른 투자이익률과 비교해볼것 10%미만이면 별로...단, 부채비율을 확인해야함.

    이익지표 ...영업현금흐름이 순이익보다 많은가 - 결과값이 음수인가..

    FCF는 영업현금흐름에서 자본적 지출(유·무형투자 비용)을 차감한 순수한 현금력이라 할 수 있다.
    말 그대로 자유롭게(Free) 사용할 수 있는 여윳돈을 뜻한다.
    잉여현금흐름이 플러스라면 미래의 투자나 채무상환에 쓸 재원이 늘어난 것이다.
    CAPEX(Capital expenditures)는 미래의 이윤을 창출하기 위해 지출된 비용을 말한다.
    이는 기업이 고정자산을 구매하거나, 유효수명이 당회계년도를 초과하는 기존의 고정자산에 대한 투자에 돈이 사용될 때 발생한다.

    잉여현금흐름이 마이너스일때는 설비투자가 많은 시기라 주가가 약세이며 이후 설비투자 마무리되면서 주가가 상승할수 있다.
    주가는 잉여현금흐름이 증가할때 상승하는 경향이 있다.
    fcf = 영업현금흐름 - capex

    가치지표평가
    price to fcf 계산
    https://www.investopedia.com/terms/p/pricetofreecashflow.asp
    pcr보다 정확하게 주식의 가치를 평가할수 있음. 10배이하 추천
    """
    redis_name = code + page + '_eval_' + 'mil'
    try:
        cached_data = Base.redis_client.get(redis_name).decode('utf-8')
    except AttributeError:
        # redis에 해당하는 값이 없는 경우
        data = eval.mil(code)
        data['score'] = score.mil(code)
        # print(data)
        if data:
            # 데이터를 Redis에 캐싱
            Base.redis_client.set(redis_name, json.dumps(data))
            # 60분후 키가 자동으로 제거됨
            Base.redis_client.expire(redis_name, 3600)
        print("analysers.eval 데이터 계산하기 - myredis.mil")
        return data
    else:
        print(f"Redis 캐시에서 데이터 가져오기(남은시간:{Base.redis_client.ttl(redis_name)}초) - myredis.mil")
        return json.loads(cached_data)


def blue_n_score(code: str) -> dict:
    """
    redis 사용 - 소멸타이머 사용
    리턴값
    {
    'date': [각 유효한 값의 최근분기 값 리스트(ex- 2020/09)],
    '순부채비율': (29.99, {'2018/12': 19.45, '2019/12': 19.52, '2020/12': 12.07, '2021/12': 82.2, '2022/12': 29.99, '2023/12': nan}),
    '순운전자본회전율': (1.04, {'2018/12': 21.91, '2019/12': 23.12, '2020/12': 5.88, '2021/12': 5.6, '2022/12': 6.04, '2023/12': nan}),
    '유동비율': 64.29,
    '이자보상배율': (-3.64, {'2018/12': 4.01, '2019/12': 1.3, '2020/12': -5.05, '2021/12': 0.56, '2022/12': -1.28, '2023/12': nan}),
    '재고자산회전율': (1.66, {'2018/12': 12.41, '2019/12': 12.44, '2020/12': 9.18, '2021/12': 9.76, '2022/12': 8.79, '2023/12': nan})
    }

    <유동비율>
    100미만이면 주의하나 현금흐름창출력이 좋으면 괜찮을수 있다.
    만약 100%이하면 유동자산에 추정영업현금흐름을 더해서 다시계산해보아 기회를 준다.
    <이자보상배율>
    이자보상배율 영업이익/이자비용으로 1이면 자금사정빡빡 5이상이면 양호
    <순운전자금회전율>
    순운전자금 => 기업활동을 하기 위해 필요한 자금 (매출채권 + 재고자산 - 매입채무)
    순운전자본회전율은 매출액/순운전자본으로 일정비율이 유지되는것이 좋으며 너무 작아지면 순운전자본이 많아졌다는 의미로 재고나 외상이 쌓인다는 뜻
    <재고자산회전율>
    재고자산회전율은 매출액/재고자산으로 회전율이 낮을수록 재고가 많다는 이야기이므로 불리 전년도등과 비교해서 큰차이 발생하면 알람.
    재고자산회전율이 작아지면 재고가 쌓인다는뜻
    <순부채비율>
    부채비율은 업종마다 달라 일괄비교 어려우나 순부채 비율이 20%이하인것이 좋고 꾸준히 늘어나지 않는것이 좋다.
    순부채 비율이 30%이상이면 좋치 않다.
    <매출액>
    매출액은 어떤경우에도 성장하는 기업이 좋다.매출이 20%씩 늘어나는 종목은 유망한 종목
    <영업이익률>
    영업이익률은 기업의 경쟁력척도로 경쟁사에 비해 높으면 경제적해자를 갖춘셈
    """
    redis_name = code + page + '_eval_' + 'blue'
    try:
        cached_data = Base.redis_client.get(redis_name).decode('utf-8')
    except AttributeError:
        # redis에 해당하는 값이 없는 경우
        data = eval.blue(code)
        data['score'] = score.blue(code)
        # print(data)
        if data:
            # 데이터를 Redis에 캐싱
            Base.redis_client.set(redis_name, json.dumps(data))
            # 60분후 키가 자동으로 제거됨
            Base.redis_client.expire(redis_name, 3600)
        print("analysers.eval 데이터 계산하기 - myredis.blue")
        return data
    else:
        print(f"Redis 캐시에서 데이터 가져오기(남은시간:{Base.redis_client.ttl(redis_name)}초) - myredis.blue")
        return json.loads(cached_data)


def growth_n_score(code: str) -> dict:
    """
    redis 사용 - 소멸타이머 사용
    리턴값
    {'date': [각 유효한 값의 최근분기 값 리스트(ex- 2020/09)],
    '매출액증가율': (-14.37, {'2018/12': -24.56, '2019/12': -20.19, '2020/12': -12.64, '2021/12': 38.65, '2022/12': -8.56, '2023/12': nan}),
    '영업이익률': {'뉴프렉스': '17.36', '동일기연': '13.58', '비에이치': '16.23', '에이엔피': '-9.30', '이브이첨단소재': '-4.93'}}

    <매출액>
    매출액은 어떤경우에도 성장하는 기업이 좋다.매출이 20%씩 늘어나는 종목은 유망한 종목
    <영업이익률>
    영업이익률은 기업의 경쟁력척도로 경쟁사에 비해 높으면 경제적해자를 갖춘셈
    """
    redis_name = code + page + '_eval_' + 'growth'
    try:
        cached_data = Base.redis_client.get(redis_name).decode('utf-8')
    except AttributeError:
        # redis에 해당하는 값이 없는 경우
        data = eval.growth(code)
        data['score'] = score.growth(code)
        # print(data)
        if data:
            # 데이터를 Redis에 캐싱
            Base.redis_client.set(redis_name, json.dumps(data))
            # 60분후 키가 자동으로 제거됨
            Base.redis_client.expire(redis_name, 3600)
        print("analysers.eval 데이터 계산하기 - myredis.growth")
        return data
    else:
        print(f"Redis 캐시에서 데이터 가져오기(남은시간:{Base.redis_client.ttl(redis_name)}초) - myredis.growth")
        return json.loads(cached_data)