import numpy as np
import random
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
import pandas as pd
import os

from attack_report import show_report

ATTACK_FILE = "attack_signal.txt"

NUM_USERS = 20
NUM_STATIONS = 5
BOUNDARY = 600
COVERAGE_RADIUS = 250

# ================= USER CONFIG =================
names = ["Aarav","Vivaan","Aditya","Arjun","Sai","Krishna","Rohan","Rahul","Kiran","Varun",
         "Ananya","Diya","Ishita","Pooja","Sneha","Meera","Kavya","Nisha","Priya","Aisha"]

providers = ["Jio","Airtel","VI","BSNL"]
devices = ["Smartphone","IoT Sensor","AR Glass","Drone","Autonomous Car"]

user_config = []
for i in range(NUM_USERS):

    if i == 1:
        user_config.append({
            "name": names[i],
            "provider": "QuantumNet",
            "device": "Quantum Processing Node",
            "network": "6G-Quantum Hybrid",
            "slice": "URLLC-Quantum",

            # 🔥 STRONG QUANTUM CONFIG
            "quantum_enabled": True,
            "qubits": 128,
            "entanglement": True,
            "superposition": True,
            "encryption": "QKD",
            "processing": "Quantum Accelerated",

            "data_rate": 2000,
            "type": "QUANTUM"
        })
    else:
        user_config.append({
            "name": names[i],
            "provider": random.choice(providers),
            "device": random.choice(devices),
            "network": "6G",
            "slice": random.choice(["URLLC","eMBB","IoT"]),
            "data_rate": random.uniform(500,1000),
            "type": "NORMAL"
        })

# ================= NETWORK =================
stations = np.random.uniform(-500, 500, (NUM_STATIONS, 2))
users = np.random.uniform(-500, 500, (NUM_USERS, 2))
velocities = np.random.uniform(-10, 10, (NUM_USERS, 2))

event_log = []
active_attacks = {}
shown_reports = set()

def get_attack_domain(attack):
    return "Quantum" if attack in ["SHOR","GROVER","QKD"] else "Classical"

def get_external_attack():
    if os.path.exists(ATTACK_FILE):
        with open(ATTACK_FILE) as f:
            lines = f.readlines()
        os.remove(ATTACK_FILE)

        attacks = []
        for line in lines:
            parts = line.strip().split(",")
            if len(parts) == 3:
                attack, attacker, victim = parts
                attacks.append((attack, int(attacker), int(victim)))
        return attacks
    return []

def nearest_station(user):
    d = np.linalg.norm(stations - user, axis=1)
    return np.argmin(d), min(d)

# ================= VISUAL =================
plt.style.use("dark_background")
plt.ion()
fig = plt.figure(figsize=(16,6))

ax1 = fig.add_subplot(131)
ax2 = fig.add_subplot(132)
ax3 = fig.add_subplot(133)

while plt.fignum_exists(fig.number):

    users[:] += velocities

    for i in range(NUM_USERS):
        for j in range(2):
            if abs(users[i][j]) > BOUNDARY:
                velocities[i][j] *= -1

    ax1.clear(); ax2.clear(); ax3.clear()
    ax1.set_facecolor("#0b0f1a")

    ax1.scatter(stations[:,0], stations[:,1], marker='^', s=300, c='cyan')
    ax1.scatter(users[:,0], users[:,1], s=80, c='yellow')

    ax1.text(-550, 550, "▲ = Base Station", color="cyan", fontsize=9)
    ax1.text(-550, 520, "● = User", color="yellow", fontsize=9)
    ax1.text(-550, 490, "U1 = Quantum Attacker", color="red", fontsize=9)

    for s in stations:
        ax1.add_patch(plt.Circle((s[0], s[1]), COVERAGE_RADIUS,
                                fill=False, linestyle='dashed',
                                alpha=0.4, color='cyan'))

    external = get_external_attack()
    for a, attacker, victim in external:
        active_attacks[victim] = (a, attacker)

    attacked_user = None

    for i, user in enumerate(users):

        sid, dist = nearest_station(user)
        latency = dist / 200
        rate = user_config[i]["data_rate"]

        ax1.text(user[0], user[1],
                 f"U{i}-{user_config[i]['name']}",
                 fontsize=6, color='white')

        # ===== BASE METRICS =====
        before_delay = latency * 100
        before_loss = random.uniform(0,5)
        before_jitter = random.uniform(0.5,5)
        before_throughput = rate

        delay = before_delay
        loss = before_loss
        jitter = before_jitter
        throughput = before_throughput

        attack_data = active_attacks.get(i, None)

        if attack_data:
            attack, attacker = attack_data
            attacked_user = i

            # NORMAL ATTACK
            if attack == "DOS":
                loss += 30; throughput *= 0.3
            elif attack == "MITM":
                jitter += 10; delay *= 2
            elif attack == "SPOOF":
                loss += 20
            elif attack == "GROVER":
                delay *= 2
            elif attack == "SHOR":
                jitter += 15
            elif attack == "QKD":
                loss += 25

            # 🔥 QUANTUM BOOST (ONLY U1)
            if user_config[attacker].get("quantum_enabled", False):

                if attack == "DOS":
                    loss += 50; throughput *= 0.2
                elif attack == "MITM":
                    jitter += 20; delay *= 3
                elif attack == "SPOOF":
                    loss += 35
                elif attack == "GROVER":
                    delay *= 3
                elif attack == "SHOR":
                    jitter += 25
                elif attack == "QKD":
                    loss += 40

            attacker_pos = users[attacker]
            ax1.plot([attacker_pos[0], user[0]],
                     [attacker_pos[1], user[1]], 'r--')

            # 🔥 REPORT (WITH NODE TYPE)
            if i not in shown_reports:
                show_report(
                    i, sid, attack, attack,
                    95, latency,
                    f"Node Type: {user_config[attacker]['type']}",
                    [delay, loss, throughput, jitter],
                    user_config[i],
                    [before_delay, before_loss, before_throughput, before_jitter],
                    get_attack_domain(attack)
                )
                shown_reports.add(i)

            event_log.append({"User":i,"BS":sid,"Type":attack})

        else:
            ax1.plot([user[0],stations[sid][0]],
                     [user[1],stations[sid][1]], color="green")

    ax1.set_xlim(-BOUNDARY,BOUNDARY)
    ax1.set_ylim(-BOUNDARY,BOUNDARY)
    ax1.set_title("⚡ 6G Quantum-Classical Network")

    ax2.axis("off")
    if attacked_user is not None:
        ax2.text(0.2,0.7,f"⚠ ATTACK ON U{attacked_user}", color='red')
    else:
        ax2.text(0.2,0.7,"SYSTEM SAFE", color='green')

    ax3.axis("off")
    ax3.set_title("Attack Log")

    y = 0.9
    for e in event_log[-8:]:
        ax3.text(0.05,y,f"U{e['User']} → BS{e['BS']} | {e['Type']}", color='white')
        y -= 0.08

    plt.pause(0.4)

plt.ioff()
plt.show()
