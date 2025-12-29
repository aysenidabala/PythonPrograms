# -*- coding: utf-8 -*-

import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl


def build_fuzzy_brake_system():
    # Evrenler (üst sınır dahil olsun diye +1)
    mesafe = ctrl.Antecedent(np.arange(0, 51, 1), "mesafe")          # 0..50
    hiz = ctrl.Antecedent(np.arange(0, 101, 1), "hiz")               # 0..100
    fren_basinci = ctrl.Consequent(np.arange(0, 101, 1), "fren_basinci")  # 0..100

    # Üyelik fonksiyonları
    mesafe["çok yakın"] = fuzz.trimf(mesafe.universe, [0, 0, 10])
    mesafe["yakın"] = fuzz.trimf(mesafe.universe, [5, 15, 25])
    mesafe["uzak"] = fuzz.trimf(mesafe.universe, [20, 30, 40])
    mesafe["çok uzak"] = fuzz.trimf(mesafe.universe, [35, 50, 50])

    hiz["çok yavaş"] = fuzz.trapmf(hiz.universe, [0, 0, 20, 30])
    hiz["yavaş"] = fuzz.trapmf(hiz.universe, [20, 30, 45, 55])
    hiz["hızlı"] = fuzz.trapmf(hiz.universe, [45, 55, 70, 80])
    hiz["çok hızlı"] = fuzz.trapmf(hiz.universe, [70, 80, 100, 100])

    fren_basinci["çok düşük"] = fuzz.trimf(fren_basinci.universe, [0, 20, 40])
    fren_basinci["düşük"] = fuzz.trimf(fren_basinci.universe, [20, 40, 60])
    fren_basinci["yüksek"] = fuzz.trimf(fren_basinci.universe, [40, 60, 80])
    fren_basinci["çok yüksek"] = fuzz.trimf(fren_basinci.universe, [60, 100, 100])

    # Kurallar
    kurallar = [
        ctrl.Rule(mesafe["çok yakın"] & hiz["çok yavaş"], fren_basinci["çok yüksek"]),
        ctrl.Rule(mesafe["yakın"] & hiz["çok yavaş"], fren_basinci["çok düşük"]),
        ctrl.Rule(mesafe["çok yakın"] & hiz["yavaş"], fren_basinci["çok yüksek"]),
        ctrl.Rule(mesafe["yakın"] & hiz["yavaş"], fren_basinci["düşük"]),
        ctrl.Rule(mesafe["uzak"] & hiz["yavaş"], fren_basinci["çok düşük"]),
        ctrl.Rule(mesafe["çok yakın"] & hiz["hızlı"], fren_basinci["çok yüksek"]),
        ctrl.Rule(mesafe["yakın"] & hiz["hızlı"], fren_basinci["düşük"]),
        ctrl.Rule(mesafe["uzak"] & hiz["hızlı"], fren_basinci["çok düşük"]),
        ctrl.Rule(mesafe["çok yakın"] & hiz["çok hızlı"], fren_basinci["çok yüksek"]),
        ctrl.Rule(mesafe["yakın"] & hiz["çok hızlı"], fren_basinci["yüksek"]),
        ctrl.Rule(mesafe["uzak"] & hiz["çok hızlı"], fren_basinci["düşük"]),
        ctrl.Rule(mesafe["çok uzak"] & hiz["çok hızlı"], fren_basinci["çok düşük"]),
    ]

    sistem = ctrl.ControlSystem(kurallar)
    return sistem


def compute_brake(speed_kmh: float, distance_m: float) -> tuple[float, float]:
    # Aralık dışını kırp (model evrenleri 0-100, 0-50)
    v = float(np.clip(speed_kmh, 0, 100))
    s = float(np.clip(distance_m, 0, 50))

    # Basit eşik: mesafe yeterliyse fren yok
    if v / 2 <= s:
        return 0.0, v

    sistem = build_fuzzy_brake_system()
    sim = ctrl.ControlSystemSimulation(sistem)
    sim.input["hiz"] = v
    sim.input["mesafe"] = s
    sim.compute()

    basinç = float(sim.output["fren_basinci"])
    yeni_hiz = max(0.0, v * (1 - basinç / 100.0))
    return basinç, yeni_hiz


def _read_int(prompt: str, min_val: int, max_val: int) -> int:
    while True:
        try:
            x = int(input(prompt).strip())
            if min_val <= x <= max_val:
                return x
            print(f"Lütfen {min_val}-{max_val} arasında bir değer gir.")
        except ValueError:
            print("Geçersiz giriş. Sayı girmen gerekiyor.")


if __name__ == "__main__":
    v = _read_int("Hızı gir (0-100 km/h): ", 0, 100)
    s = _read_int("Mesafeyi gir (0-50 m): ", 0, 50)

    basinç, yeni_hiz = compute_brake(v, s)

    if basinç == 0.0:
        print("Fren basılması gerek yoktur.")
    else:
        print("Fren basıncı (%):", round(basinç, 2))
        print("Yeni hız değeri:", round(yeni_hiz, 2))
