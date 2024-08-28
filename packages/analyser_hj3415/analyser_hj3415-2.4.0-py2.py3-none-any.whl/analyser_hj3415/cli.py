import argparse
from utils_hj3415 import noti


def analyser():
    from analyser_hj3415.myredis import red_ranking
    commands = {
        'ranking': red_ranking
    }
    parser = argparse.ArgumentParser()
    parser.add_argument('command', help=f"Commands - {commands.keys()}")
    parser.add_argument('--noti', action='store_true', help='작업완료후 메시지 전송여부')

    args = parser.parse_args()

    if args.command in commands.keys():
        if args.command == 'ranking':
            print(commands['ranking']())
            if args.noti:
                noti.telegram_to('manager', "오늘의 red ranking을 저장했습니다.(유효 12시간)")
    else:
        print(f"The command should be in {list(commands.keys())}")


