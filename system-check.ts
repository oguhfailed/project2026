type Component =
  | string
  | number
  | { type: "sensor"; status: string }
  | { type: "motor"; speed: number }
  | null;

function getComponentInfo(component: Component): string {
  if (component === null) {
    return "Component is null";
  }
  if (typeof component === "string") {
    return `String component: ${component}`;
  }
  if (typeof component === "number") {
    return `Numeric component: ${component}`;
  }
  if (component.type === "sensor") {
    return `Sensor status: ${component.status}`;
  }
  return `Motor speed: ${component.speed}`;
}
