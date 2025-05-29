# 과정 4 - (문제9) "비료 자동 투입기"

import matplotlib.pyplot as plt
import matplotlib

matplotlib.rc('font', family='AppleGothic')
plt.rcParams['axes.unicode_minus'] = False

class Stack:
    def __init__(self, max_size=10):
        self.items = []
        self.max_size = max_size

    def push(self, item):
        if len(self.items) >= self.max_size:
            print('[경고] 스택이 가득 찼습니다. 더 이상 push할 수 없습니다.\n')
        else:
            self.items.append(item)
            print(f'[push] {item} 추가됨\n')

    def pop(self):
        if self.empty():
            print('[경고] 스택이 비어있습니다. pop할 수 없습니다.\n')
            return None
        else:
            item = self.items.pop()
            print(f'[pop] {item} 제거됨\n')
            return item

    def peek(self):
        if self.empty():
            print('[경고] 스택이 비어있습니다. 확인할 수 없습니다.\n')
            return None
        else:
            print(f'[peek] 현재 top 항목은: {self.items[-1]}\n')
            return self.items[-1]

    def empty(self):
        return len(self.items) == 0

    # [보너스 과제] - 스택 구조 클래스화 및 스택의 상태를 시각화
    def visualize(self):
        print('\n[Stack 시각화]')
        fig, ax = plt.subplots(figsize=(6, 6))
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.axis('off')

        box_height = 1 / self.max_size

        for i in range(self.max_size):
            y = i * box_height
            if i < len(self.items):
                color = 'skyblue'
                label = self.items[i]  # 아래에서부터 위로: 맨 먼저 들어온 게 아래쪽
            else:
                color = 'white'
                label = ''
            ax.add_patch(plt.Rectangle((0, y), 1, box_height, facecolor=color, edgecolor='black'))
            ax.text(0.5, y + box_height / 2, label, va='center', ha='center', fontsize=10)

        plt.title('Stack View (Top ↑)', fontsize=14)
        plt.tight_layout()
        plt.show()

# 테스트 코드 예시
if __name__ == '__main__':
    stack = Stack()

    # 1~10까지 push
    for i in range(1, 12):
        stack.push(f'비료- {i:d}')

    stack.peek()
    stack.pop()
    stack.peek()

    print('[empty 확인]:', '비어있음\n' if stack.empty() else '비어있지 않음\n')

    stack.visualize()