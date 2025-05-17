# 과정 2 - (문제2) "카이사르의 암호"

def caesar_cipher_decode(target_text):
    alphabet = "abcdefghijklmnopqrstuvwxyz"
    # (보너스 과제) 사전 단어 포함 시 자동 판단
    dict_words = ["the", "this", "that", "and", "you", "password", "flag"]
    found_shift = None

    for shift in range(26):
        decoded = ""
        for ch in target_text:
            if ch.isalpha():
                is_upper = ch.isupper()
                ch_lower = ch.lower()
                idx = (alphabet.index(ch_lower) - shift) % 26
                new_ch = alphabet[idx]
                decoded += new_ch.upper() if is_upper else new_ch
            else:
                decoded += ch

        print(f"[{shift}] {decoded}\n")

        for word in dict_words:
            if word in decoded.lower():
                print(f"단어 '{word}' 발견됨 — shift {shift}가 유력합니다.")
                found_shift = shift
                break
        if found_shift is not None:
            break

    return found_shift


def main():
    try:
        with open("src/Process2/2-2/password.txt", "r") as f:
            encrypted = f.read().strip()
    except Exception as e:
        print(f"오류 발생: {e}")
        return
    
    found_shift = caesar_cipher_decode(encrypted)

    try:
        choice = input("\n저장할 shift 번호를 입력: ").strip()
        if choice == "" and found_shift is not None:
            choice = str(found_shift)
        if choice.isdigit():
            shift = int(choice)
            if 0 <= shift < 26:
                alphabet = "abcdefghijklmnopqrstuvwxyz"
                decoded = ""
                for ch in encrypted:
                    if ch.isalpha():
                        is_upper = ch.isupper()
                        ch_lower = ch.lower()
                        idx = (alphabet.index(ch_lower) - shift) % 26
                        new_ch = alphabet[idx]
                        decoded += new_ch.upper() if is_upper else new_ch
                    else:
                        decoded += ch
                with open("src/Process2/2-2/result.txt", "w") as f:
                    f.write(decoded)
                print(f"'result.txt' 저장(shift {shift})")
            else:
                print("shift 범위는 0~25 사이")
        else:
            print("저장하지 않고 종료...")
    except Exception as e:
        print(f"오류 발생: {e}")

if __name__ == "__main__":
    main()