import time
import random

ATTACK_FILE = "attack_signal.txt"

attacks = {
    "1": ("DOS", "Network flooding attack"),
    "2": ("MITM", "Man-in-the-middle interception"),
    "3": ("SPOOF", "Identity spoofing"),
    "4": ("GROVER", "Quantum brute-force acceleration"),
    "5": ("SHOR", "Quantum cryptographic break"),
    "6": ("QKD", "Quantum key interception")
}

ATTACKER = 1  # Quantum attacker

def send_attack(attack, victim):
    with open(ATTACK_FILE, "a") as f:
        f.write(f"{attack},{ATTACKER},{victim}\n")

# 🔥 FAKE REAL-TIME NETWORK TRAFFIC (SAFE SIMULATION)
def simulate_traffic(victim):
    print("\n📡 Capturing live user traffic...")
    for i in range(5):
        latency = round(random.uniform(50, 300), 2)
        packets = random.randint(100, 500)
        print(f"[Packet {i+1}] Latency: {latency} ms | Data: {packets} KB")
        time.sleep(0.4)

def quantum_effect(attack):
    print("\n🧠 Quantum Processing Layer Activated...")
    time.sleep(0.5)

    if attack == "GROVER":
        print("⚡ Reducing search complexity using Grover acceleration...")
    elif attack == "SHOR":
        print("🔐 Breaking cryptographic keys using Shor algorithm...")
    elif attack == "QKD":
        print("🔑 Intercepting quantum key distribution channel...")

    time.sleep(1)

def classical_effect(attack):
    print("\n⚙ Classical Attack Engine Running...")
    time.sleep(0.5)

    if attack == "DOS":
        print("🌐 Flooding network with high traffic packets...")
    elif attack == "MITM":
        print("🕵 Intercepting communication between nodes...")
    elif attack == "SPOOF":
        print("🎭 Spoofing identity and injecting fake packets...")

    time.sleep(1)

def simulate_attack(attack, victim):
    print("\n======================================")
    print("⚡ Initializing Attack Sequence...")
    print("======================================")

    time.sleep(1)

    print(f"\n🎯 Target Locked: User U{victim}")
    time.sleep(0.5)

    simulate_traffic(victim)

    # 🔥 DIFFERENT BEHAVIOR
    if attack in ["GROVER", "SHOR", "QKD"]:
        quantum_effect(attack)
    else:
        classical_effect(attack)

    print("\n🚀 Deploying Attack Payload...")
    for i in range(3):
        print(f"Injecting packets... {i+1}/3")
        time.sleep(0.5)

    print("\n🚨 ATTACK SUCCESSFULLY DEPLOYED")
    print("--------------------------------------")
    print(f"Attacker: U{ATTACKER} (Quantum System)")
    print(f"Victim: U{victim}")
    print(f"Attack Type: {attack}")
    print("--------------------------------------\n")

    send_attack(attack, victim)

def main():
    print("\n===== 6G QUANTUM ATTACK CONTROL SYSTEM =====")

    while True:
        print("\nSelect Attack:")
        for k, v in attacks.items():
            print(f"{k}. {v[0]}")

        print("7. Exit")

        choice = input("Enter choice: ")

        if choice == "7":
            print("Exiting...")
            break

        if choice not in attacks:
            print("Invalid choice")
            continue

        attack = attacks[choice][0]

        try:
            victim = int(input("Enter Victim User ID (0-19): "))
        except:
            print("Invalid input")
            continue

        simulate_attack(attack, victim)

main()
