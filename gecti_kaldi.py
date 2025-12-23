not1 = int(input("Notu girin (0-100): "))

if not1 < 0 or not1 > 100:
    print("Öyle bir not yok")
elif not1 >= 50:
    print("Geçti.")
else:
    print("Kaldı.")