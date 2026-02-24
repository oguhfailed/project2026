type FriendlyAlien = { name: string; greeting: string };
type HostileAlien = { name: string; weapon: string };
type AlienContact = FriendlyAlien | HostileAlien;

function handleEncounter(contact: AlienContact): void {
  if ("greeting" in contact) {
    console.log(`Friendly alien ${contact.name} says: ${contact.greeting}`);
  } else {
    console.log(`Hostile alien ${contact.name} is armed with: ${contact.weapon}`);
  }
}
