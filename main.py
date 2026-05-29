import secrets

# Большое простое число (для работы с текстом до ~60 символов)
P = 2**521 - 1

def split(text, k, n):
    s = int.from_bytes(text.encode(), 'big')
    coeffs = [s] + [secrets.randbelow(P) for _ in range(k - 1)]
    def f(x):
        res = 0
        for c in reversed(coeffs): res = (res * x + c) % P
        return res
    return [(i, f(i)) for i in range(1, n + 1)]

def recover(shares):
    secret = 0
    for i, (xi, yi) in enumerate(shares):
        num, den = 1, 1
        for j, (xj, yj) in enumerate(shares):
            if i == j: continue
            num = (num * -xj) % P
            den = (den * (xi - xj)) % P
        secret = (secret + yi * num * pow(den, -1, P)) % P
    return secret.to_bytes((secret.bit_length() + 7) // 8, 'big').decode(errors='ignore')

def main():
    while True:
        print(f"\n--- СХЕМА ШАМИРА ---")
        act = input("1. Разделить секрет\n2. Собрать секрет\n0. Выход\n> ")
        
        if act == '1':
            text = input("Введите текст: ")
            n = int(input("На сколько частей (n): "))
            k = int(input("Порог сборки (k): "))
            shares = split(text, k, n)
            print("\nВаши части (сохраните их):")
            for s in shares: print(f"Часть {s[0]}: {s[1]}")
            
        elif act == '2':
            k = int(input("Сколько частей у вас есть? "))
            shares = []
            for _ in range(k):
                raw = input("Введите часть в формате 'номер значение': ").split()
                shares.append((int(raw[0]), int(raw[1])))
            print(f"\nРезультат: {recover(shares)}")
            
        elif act == '0': break

if __name__ == "__main__":
    main()