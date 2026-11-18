import csv
from pathlib import Path

START_DIAL = 240.0
STEP = 14.0
NUM_STEPS = 25  # 0 to 360 degrees inclusive
V_BG = 0.313


def record_series(series_name: str, filename: str) -> None:
    print(f"\n=== Recording {series_name} (V_bg = {V_BG} V) ===")
    print("Type the voltage reading and press Enter (or 'u' to undo last step):\n")

    rows = []
    i = 0
    while i < NUM_STEPS:
        theta = i * STEP
        dial_angle = (START_DIAL + theta) % 360.0
        raw = input(
            f"[{i + 1:02d}/{NUM_STEPS}] Set dial to {dial_angle:5.1f}° (θ = {theta:5.1f}°) -> V [V]: "
        ).strip()

        if raw.lower() == "u":
            if rows:
                rows.pop()
                i -= 1
                print("  ↩ Undid previous measurement.")
            else:
                print("  Nothing to undo.")
            continue

        try:
            voltage = float(raw)
        except ValueError:
            print("  Invalid number, try again.")
            continue

        v_net = round(voltage - V_BG, 6)
        rows.append(
            {
                "theta_deg": theta,
                "dial_deg": dial_angle,
                "V_raw": voltage,
                "V_net": v_net,
            }
        )
        i += 1

    out_path = Path(filename)
    with out_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f, fieldnames=["theta_deg", "dial_deg", "V_raw", "V_net"]
        )
        writer.writeheader()
        writer.writerows(rows)

    print(f"\nSaved {len(rows)} rows to {out_path.resolve()}")


if __name__ == "__main__":
    mode = input("Which component are you measuring? [H / V]: ").strip().upper()
    if mode == "H":
        record_series("Horizontal Component (I_H)", "malus_horizontal.csv")
    elif mode == "V":
        record_series("Vertical Component (I_V)", "malus_vertical.csv")
    else:
        print("Please run again and enter H or V.")
