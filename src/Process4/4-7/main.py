# 과정 4 - (문제7) "끊기지 않는 음악"

import os
import time

class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

class CircularLinkedList:
    def __init__(self):
        self.tail = None  # 마지막 노드를 가리킴
        self.current = None  # get_next용 포인터

    def insert(self, data):
        new_node = Node(data)
        if self.tail is None:
            self.tail = new_node
            new_node.next = new_node
            self.current = new_node
        else:
            new_node.next = self.tail.next
            self.tail.next = new_node
            self.tail = new_node

    def delete(self, data):
        if self.tail is None:
            print('리스트가 비어 있습니다.')
            return

        prev = self.tail
        curr = self.tail.next

        while True:
            if curr.data == data:
                if curr == self.tail:
                    if curr.next == curr:
                        self.tail = None
                        self.current = None
                    else:
                        prev.next = curr.next
                        self.tail = prev
                else:
                    prev.next = curr.next
                print(f'"{data}" 삭제 완료')
                return
            prev, curr = curr, curr.next
            if curr == self.tail.next:
                break
        print(f'"{data}" 를 찾을 수 없습니다.')

    def get_next(self):
        if self.current is None:
            print('리스트가 비어 있습니다.')
            return None
        self.current = self.current.next
        return self.current.data

    def search(self, keyword):
        if self.tail is None:
            return []

        result = []
        curr = self.tail.next
        while True:
            if keyword.lower() in curr.data.lower():
                result.append(curr.data)
            curr = curr.next
            if curr == self.tail.next:
                break
        return result

    def display(self, count=10):
        if self.tail is None:
            print('[빈 리스트]')
            return

        curr = self.tail.next
        for _ in range(count):
            print(curr.data)
            curr = curr.next


if __name__ == '__main__':
    circularlist = CircularLinkedList()

    # 예시: 멜론 인기곡 6곡
    songs = [
        '10CM - 너에게 닿기를',
        '제니 (JENNIE) - like JENNIE',
        'WOODZ - Drowning',
        'DAY6 - Maybe Tomorrow',
        'aespa - Whiplash',
        'LE SSERAFIM - HOT'
    ]

    for song in songs:
        circularlist.insert(song)

    print()
    for _ in range(10):
        print('▶', circularlist.get_next())
        time.sleep(1)

    print('\n"JENNIE" 검색 결과:')
    for result in circularlist.search('JENNIE'):
        print('▶', result)

    print('\nWOODZ - Drowning 삭제:')
    circularlist.delete('WOODZ - Drowning')

    print('\n삭제 이후 원형 연결 리스트 상태:')
    circularlist.display(6)
    print()

# # [보너스 과제] - 노래 제목 말고 실제 mp3 등의 파일 목록을 입력하고 순차적으로 음악이 재생하도록 음악 플레이어 생성
# from playsound import playsound

# def play_music_files(circularlist):
#     while True:
#         song = circularlist.get_next()
#         print('🎵 Now playing:', song)
#         playsound(song)  # mp3 파일 경로일 경우
#         time.sleep(1)