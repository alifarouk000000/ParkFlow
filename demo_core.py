"""
ParkFlow - console demo for Ali's core (no Streamlit needed).
Run:  python demo_core.py
"""
from core import ParkingSystem, get_algorithms_status

ps = ParkingSystem(number_of_slots=5, slots_per_row=5)   # P01 Compact .. P05 Oversized
T = "2026-10-15 08:00"

print("=== 1) Arrivals ===")
for plate, vtype in [("ABC 1234", "Car"), ("MOT 7", "Motorcycle"), ("TRK 44", "Truck"),
                     ("EV 900", "Electric Vehicle"), ("سصع552", "Car"), ("TRK 55", "Truck")]:
    print(" ", ps.park_vehicle(plate, vtype, now=T)["message"])

print("\n=== 2) Invalid input (handled, no crash) ===")
print(" ", ps.park_vehicle("12", "Car")["message"])
print(" ", ps.park_vehicle("abc-1234", "Car")["message"])
print(" ", ps.park_vehicle("NEW 1", "Plane")["message"])
print(" ", ps.exit_vehicle("XYZ 9")["message"])

print("\n=== 3) Parking map (2D grid, 1 = occupied) ===")
for row in ps.get_occupancy_matrix():
    print(" ", row)
print("  waiting:", [v.plate_number for v in ps.get_waiting_vehicles()])

print("\n=== 4) Exit + fee + queue served ===")
res = ps.exit_vehicle("TRK 44", now="2026-10-15 10:30")
print(" ", res["message"])
print("  served from queue:", [v["plate_number"] for v in res["served_from_queue"]])
print(" ", ps.exit_vehicle("EV 900", now="2026-10-15 09:10")["message"])

print("\n=== 5) Search / sort ===")
print("  hash lookup  :", ps.find_vehicle("abc1234"))
print("  binary search:", ps.find_record_by_id("V0002"))
print("  partial 'trk':", [r["plate_number"] for r in ps.search_vehicles("trk")])
print("  sorted by fee:", [(r["plate_number"], r["fee"]) for r in ps.sort_records("fee", descending=True)])

print("\n=== 6) Undo ===")
print(" ", ps.undo_last_operation()["message"])

print("\n=== 7) Status ===")
s = ps.get_parking_status()
print(f"  total={s['total']} occupied={s['occupied']} available={s['available']} "
      f"waiting={s['waiting']} occupancy={s['occupancy_rate']}%")

print("\n=== 8) History (oldest first) ===")
for h in ps.get_history():
    print(f"  {h['time']}  {h['action']:<6} {h['plate_number']:<10} {h['slot_id'] or ''} {h['details']}")

print("\n=== Algorithms source ===")
for name, src in get_algorithms_status().items():
    print(f"  {'OK ' if src == 'team' else '!! '} {name}: {src}")
