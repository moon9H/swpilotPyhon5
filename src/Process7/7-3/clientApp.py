# 과정 7 - (문제3) 완전히 작동하는 To-Do
# 보너스 과제 - 구현한 기능들을 호출해서 동작하는 간단한 클라이언트 앱
import requests

BASE_URL = "http://127.0.0.1:8000"

def add_todo(ID, item):
    response = requests.post(f"{BASE_URL}/add_todo", json={"id": ID, "item": item})
    if response.status_code == 200:
        print("Todo added:", response.json())
    else:
        print("Failed to add todo:", response.json())

def retrieve_todos():
    response = requests.get(f"{BASE_URL}/retrieve_todo")
    if response.status_code == 200:
        print("Todo list:", response.json())
    else:
        print("Failed to retrieve todos:", response.json())

def get_single_todo(ID):
    response = requests.get(f"{BASE_URL}/get_single_todo/{ID}")
    if response.status_code == 200:
        print("Todo retrieved:", response.json())
    else:
        print("Failed to retrieve todo:", response.json())

def update_todo(ID, item):
    response = requests.put(f"{BASE_URL}/update_todo/{ID}", json={"item": item})
    if response.status_code == 200:
        print("Todo updated:", response.json())
    else:
        try:
            print("Failed to update todo:", response.json())
        except requests.exceptions.JSONDecodeError:
            print("Failed to update todo: No JSON response received. Status code:", response.status_code)

def delete_todo(ID):
    response = requests.delete(f"{BASE_URL}/delete_single_todo/{ID}")
    if response.status_code == 200:
        print("Todo deleted:", response.json())
    else:
        print("Failed to delete todo:", response.json())

if __name__ == "__main__":
    # Test
    print("Adding todos:")
    add_todo(1, "Give Water To Plants")
    add_todo(2, "Communicate With Earth")
    
    print("\nRetrieving all todos:")
    retrieve_todos()
    
    print("\nGetting single todo (ID 1):")
    get_single_todo(1)
    
    print("\nUpdating todo (ID 1):")
    update_todo(1, "Give Water To Groceries")
    
    print("\nGetting updated single todo (ID 1):")
    get_single_todo(1)
    
    print("\nDeleting todo (ID 1):")
    delete_todo(1)
    
    print("\nRetrieving all todos after deletion:")
    retrieve_todos()