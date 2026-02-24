type Timestamp = { timestamp: Date };

type Destination = { planetName: string; sector: string } & Timestamp;
type WarpDrive = { warpFactor: number } & Timestamp;
type NavigationCommand = Destination | WarpDrive;

const destination: Destination = {
  planetName: "Mars",
  sector: "Alpha-7",
  timestamp: new Date(),
};

const warpDrive: WarpDrive = {
  warpFactor: 9,
  timestamp: new Date(),
};

const navigationCommand: NavigationCommand = destination;
