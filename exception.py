class selfException(Exception):    # Exception을 상속받아서 새로운 예외를 만듦
    def __init__(self):
        super().__init__('강제종료')

class abortException(Exception):
    def __init__(self):
        super().__init__("중단")

class saveStopException(Exception):
    def __init__(self):
        super().__init__("저장 중단")

class NofoundException(Exception):
    def __init__(self):
        super().__init__("없음")

class NofoundSessionException(Exception):
    def __init__(self):
        super().__init__("세션없음")

class changeException(Exception):
    def __init__(self):
        super().__init__("선수 다시 검색")