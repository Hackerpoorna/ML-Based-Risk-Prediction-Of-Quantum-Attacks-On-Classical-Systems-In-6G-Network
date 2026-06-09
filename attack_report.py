import tkinter as tk

# ================= ML-STYLE REASONING =================
def ml_reasoning(before, after):
    reasons = []

    d0, l0, t0, j0 = before
    d1, l1, t1, j1 = after

    delta = {
        "Latency": d1 - d0,
        "Packet Loss": l1 - l0,
        "Throughput": t1 - t0,
        "Jitter": j1 - j0
    }

    # sort by highest impact
    sorted_features = sorted(delta.items(), key=lambda x: abs(x[1]), reverse=True)

    for feature, value in sorted_features:

        if abs(value) < 1:
            continue

        if feature == "Latency" and value > 0:
            reasons.append(f"Latency increased by {value:.2f} ms indicating delay anomaly")

        elif feature == "Packet Loss" and value > 5:
            reasons.append(f"Packet loss increased by {value:.2f}% suggesting network disruption")

        elif feature == "Throughput" and value < 0:
            reasons.append(f"Throughput dropped by {abs(value):.2f} Mbps indicating resource degradation")

        elif feature == "Jitter" and value > 2:
            reasons.append(f"Jitter increased by {value:.2f} ms indicating unstable transmission")

    if not reasons:
        reasons.append("No significant deviation detected")

    return reasons


# ================= SEVERITY CALCULATION =================
def calculate_severity(before, after):
    d0, l0, t0, j0 = before
    d1, l1, t1, j1 = after

    score = 0

    score += min((l1 - l0) / 10, 4)
    score += min((j1 - j0) / 5, 3)
    score += min((d1 - d0) / 50, 2)
    score += min(abs(t1 - t0) / 200, 3)

    return int(min(score, 10))


# ================= REPORT =================
def show_report(user, station, attack, prediction, confidence,
                latency, reason, after, user_info, before, domain):

    d0, l0, t0, j0 = before
    d1, l1, t1, j1 = after

    severity = calculate_severity(before, after)
    reasons = ml_reasoning(before, after)

    # ================= UI =================
    window = tk.Tk()
    window.title("6G AI Threat Intelligence Report")
    window.geometry("820x720")
    window.configure(bg="#0f172a")

    def add(text, color="white", bold=False):
        font = ("Arial",11,"bold") if bold else ("Arial",11)
        tk.Label(window, text=text,
                 fg=color, bg="#0f172a",
                 font=font, anchor="w",
                 justify="left", wraplength=780).pack(fill="x", padx=12, pady=2)

    # HEADER
    tk.Label(window, text="AI-DRIVEN 6G CYBER THREAT REPORT",
             fg="cyan", bg="#0f172a",
             font=("Arial",16,"bold")).pack(pady=10)

    # USER
    add("User Profile", "cyan", True)
    add(f"User: U{user} | {user_info['name']}")
    add(f"Device: {user_info['device']} | Network: {user_info['network']}")

    add("--------------------------------------------------")

    # PREDICTION
    add("Prediction", "yellow", True)
    add(f"Attack Type: {attack} ({domain})")
    add(f"Confidence: {confidence}%")
    add(f"Severity Score: {severity}/10")

    add("--------------------------------------------------")

    # BEFORE
    add("Baseline", "cyan", True)
    add(f"Latency: {d0:.2f} ms | Loss: {l0:.2f}% | Throughput: {t0:.0f} Mbps | Jitter: {j0:.2f} ms")

    # AFTER
    add("Observed", "red", True)
    add(f"Latency: {d1:.2f} ms | Loss: {l1:.2f}% | Throughput: {t1:.0f} Mbps | Jitter: {j1:.2f} ms")

    add("--------------------------------------------------")

    # IMPACT
    add("Impact Analysis", "yellow", True)
    add(f"Latency Δ: {d1-d0:.2f} ms")
    add(f"Loss Δ: {l1-l0:.2f}%")
    add(f"Throughput Δ: {t1-t0:.2f} Mbps")
    add(f"Jitter Δ: {j1-j0:.2f} ms")

    add("--------------------------------------------------")

    # REASONING
    add("AI Decision Reasoning", "cyan", True)

    add(f"ML Insight: {reason}", "yellow")

    for r in reasons:
        add(f"• {r}")

    add("--------------------------------------------------")

    # FINAL VERDICT (IMPROVED)
    add("Final Verdict", "red", True)

    if severity >= 7:
        verdict = "High Impact Attack Detected"
    elif severity >= 4:
        verdict = "Moderate Impact Attack Detected"
    else:
        verdict = "Low Impact Anomaly"

    if confidence > 90:
        verdict += " (High Confidence)"
    elif confidence > 70:
        verdict += " (Moderate Confidence)"
    else:
        verdict += " (Low Confidence)"

    add(verdict)

    window.mainloop()
