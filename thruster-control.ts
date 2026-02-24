type Thruster = { name: string; powerLevel: number };
type Thrusters = { left: Thruster; right: Thruster; main: Thruster };

const thrusters: Thrusters = {
  left: { name: "left", powerLevel: 0 },
  right: { name: "right", powerLevel: 0 },
  main: { name: "main", powerLevel: 0 },
};

function setThrusterPower(thruster: "left" | "right" | "main", powerLevel: number): string {
  if (!["left", "right", "main"].includes(thruster)) {
    throw new Error(`Invalid thruster: ${thruster}`);
  }
  if (powerLevel < 0 || powerLevel > 100) {
    throw new Error(`Power level must be between 0 and 100`);
  }
  thrusters[thruster].powerLevel = powerLevel;
  return `Thruster '${thruster}' set to power level ${powerLevel}`;
}
