import subprocess
import os
import json
from datetime import datetime

class PatchManager:
    def __init__(self, config_file):
        with open(config_file, 'r') as f:
            self.config = json.load(f)

    def check_for_updates(self):
        print("Checking for updates...")
        subprocess.run(["sudo", "apt", "update"])

    def list_available_updates(self):
        print("Listing available updates...")
        result = subprocess.run(["apt", "list", "--upgradable"], capture_output=True, text=True)
        return result.stdout.splitlines()

    def apply_patches(self, packages):
        print(f"Applying patches for: {', '.join(packages)}")
        subprocess.run(["sudo", "apt", "install", "-y"] + packages)

    def generate_report(self, packages):
        report = f"Patch Report - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
        report += f"Applied patches: {', '.join(packages)}\n"
        return report

    def run(self):
        self.check_for_updates()
        updates = self.list_available_updates()
        if updates:
            packages_to_update = [u.split('/')[0] for u in updates if u.split('/')[0] in self.config['allowed_packages']]
            if packages_to_update:
                self.apply_patches(packages_to_update)
                report = self.generate_report(packages_to_update)
                with open(self.config['report_file'], 'w') as f:
                    f.write(report)
                print(f"Patches applied and report generated: {self.config['report_file']}")
            else:
                print("No allowed packages to update.")
        else:
            print("No updates available.")

if __name__ == "__main__":
    manager = PatchManager("config.json")
    manager.run()
