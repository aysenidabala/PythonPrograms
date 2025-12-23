sayilar = []
toplam = 0

for i in range(5):
    giris = int(input(f"{i+1}. sayıyı girin: ")) 
    sayilar.append(giris)
    toplam += giris
    

# en büyük / en küçük
en_buyuk = sayilar[0]
en_kucuk = sayilar[0]
for s in sayilar[1:]:
    if s > en_buyuk:
        en_buyuk = s
    if s < en_kucuk:
        en_kucuk = s

# ortalama
ortalama = toplam / len(sayilar)

print("Liste:", sayilar)
print("En büyük sayı:", en_buyuk)
print("En küçük sayı:", en_kucuk)
print("Ortalama:", ortalama)
print("Tersten liste:", list(reversed(sayilar)))
