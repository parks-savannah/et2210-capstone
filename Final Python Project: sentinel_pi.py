import random
import datetime
import time
import csv
from abc import ABC, abstractmethod

# --- STRATEGY PATTERN: ALERT BEHAVIORS ---
class AlertStrategy(ABC):
    @abstractmethod
    def alert(self, distance): pass

class SilentLogStrategy(AlertStrategy):
    def alert(self, distance): 
        return f"LOW: Breach at {distance:.2f}cm"

class HighFrequencyStrategy(AlertStrategy):
    def alert(self, distance): 
        return f"CRITICAL: BREACH AT {distance:.2f}cm"

# --- STATE PATTERN: SYSTEM MODES ---
class SystemState(ABC):
    @abstractmethod
    def evaluate(self, distance): pass

class DayState(SystemState):
    def evaluate(self, distance): return distance < 50.0 [cite: 107, 198]

class NightState(SystemState):
    def evaluate(self, distance): return distance < 100.0 [cite: 112, 200]

# --- CORE LOGIC ---
class AlarmController:
    def __init__(self):
        self.state = DayState() [cite: 204]
        self.strategy = SilentLogStrategy() [cite: 205]
        self.buffer = [] [cite: 206]

    def update_environment(self, light_level):
        """Adjusts sensitivity and alert strategy based on ambient light[cite: 207]."""
        if light_level < 300:
            self.state = NightState() [cite: 209]
            self.strategy = HighFrequencyStrategy() [cite: 210]
        else:
            self.state = DayState() [cite: 212]
            self.strategy = SilentLogStrategy() [cite: 213]

    def process_reading(self, distance):
        """Applies smoothing logic (Lists) and evaluates breaches[cite: 214, 307]."""
        self.buffer.append(distance) [cite: 216]
        if len(self.buffer) > 5:
            self.buffer.pop(0) [cite: 218]
        
        avg_dist = sum(self.buffer) / len(self.buffer) [cite: 219]
        if self.state.evaluate(avg_dist): [cite: 220]
            return self.strategy.alert(avg_dist) [cite: 221]
        return None

# --- DATA STRUCTURES & ALGORITHMS (FILE I/O) ---
class LogManager:
    @staticmethod
    def write_log(message, filename="security_log.csv"):
        """Persistent logging to CSV[cite: 225, 312]."""
        timestamp = datetime.datetime.now().strftime("%H:%M:%S")
        with open(filename, "a", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([timestamp, message])

    @staticmethod
    def analyze_logs(filename="security_log.csv"):
        """Demonstrates Search and Sort algorithms."""
        try:
            logs = []
            with open(filename, "r") as f:
                reader = csv.reader(f)
                logs = list(reader)

            if not logs: return

            # SORTING: Organize by severity (CRITICAL first) [cite: 310]
            logs.sort(key=lambda x: "CRITICAL" in x[1], reverse=True)
            
            print("\n--- Post-Simulation Log Analysis (Sorted by Severity) ---")
            for row in logs:
                print(f"[{row[0]}] {row[1]}")

            # SEARCH: Scan for most frequent breach type [cite: 309]
            critical_count = sum(1 for row in logs if "CRITICAL" in row[1])
            print(f"\nSearch Summary: Found {critical_count} critical incidents.")

        except FileNotFoundError:
            print("Exception: No log file found to analyze.") [cite: 311]

# --- SENSOR SIMULATION ---
class Sensor(ABC):
    def __init__(self, name, unit):
        self.name = name
        self.unit = unit
    @abstractmethod
    def get_reading(self): pass

class UltrasonicSensor(Sensor):
    def get_reading(self):
        return round(random.uniform(2.0, 400.0), 2) [cite: 141]

class LightSensor(Sensor):
    def get_reading(self):
        return random.randint(0, 1000) [cite: 144]

def main():
    print("--- Sentinel-PI: Final System Run ---")
    sonar = UltrasonicSensor("Main Entry", "cm")
    photo = LightSensor("AmbientLight", "lux")
    controller = AlarmController()
    logger = LogManager()

    try:
        for i in range(10): # Simulation cycles
            dist = sonar.get_reading()
            lux = photo.get_reading()
            controller.update_environment(lux)
            
            result = controller.process_reading(dist)
            print(f"Cycle {i+1} | Lux: {lux} | Dist: {dist}cm | Mode: {type(controller.state).__name__}")
            
            if result:
                logger.write_log(result)
            time.sleep(0.1)

        logger.analyze_logs()

    except Exception as e:
        print(f"Critical System Error: {e}") [cite: 159]

if __name__ == "__main__":
    main()
