# 과정 4 - (문제6) "음악이 필요해"

class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

class LinkedList:
    def __init__(self):
        self.head = None

    def insert(self, data, position=None):
        new_node = Node(data)

        # 1. 빈 리스트인 경우
        if self.head is None:
            self.head = new_node
            return

        # 2. 맨 앞에 삽입
        if position == 0:
            new_node.next = self.head
            self.head = new_node
            return

        # 3. 중간 또는 맨 뒤 삽입
        current = self.head
        index = 0
        prev = None
        while current and (position is None or index < position):
            prev = current
            current = current.next
            index += 1

        new_node.next = current
        if prev:
            prev.next = new_node

    def delete(self, data):
        current = self.head
        prev = None

        while current:
            if current.data == data:
                if prev is None:
                    # 삭제 대상이 head
                    self.head = current.next
                else:
                    prev.next = current.next
                return True  # 삭제 성공
            prev = current
            current = current.next

        return False  # 삭제 실패

    #[보너스 과제] - 처음부터 끝까지 순차적으로 가져오는 get_list() 함수 추가
    def get_list(self):
        result = []
        current = self.head

        while current:
            result.append(current.data)
            current = current.next

        return result


# 사용 예시
if __name__ == '__main__':
    playlist = LinkedList()

    # 음악 추가
    playlist.insert('LE SSERAFIM (르세라핌) - HOT')
    playlist.insert('DAY6 (데이식스) - Maybe Tomorrow')
    playlist.insert('WOODZ - Drowning', 2) # 중간 삽입
    playlist.insert('제니 (JENNIE) - like JENNIE', 0) # 맨 앞
    playlist.insert('10CM - 너에게 닿기를')        

    # 현재 목록 출력
    print('\n현재 재생목록:', playlist.get_list())

    # 음악 삭제
    playlist.delete('LE SSERAFIM (르세라핌) - HOT')

    print(f'\n삭제 후 재생목록: {playlist.get_list()}\n')