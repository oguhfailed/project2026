// TypeScript Intersection Types
//
// The `&` operator creates a type that must satisfy ALL combined types at once.

type Named = { name: string };
type Aged  = { age: number };

// Person must have BOTH name and age
type Person = Named & Aged;

const alice: Person = {
  name: "Alice",
  age: 30,
};

console.log(alice); // { name: 'Alice', age: 30 }

// ─── Generic mixin example ───────────────────────────────────────────────────

// Adds timestamp fields to any existing type T
type WithTimestamp<T> = T & { createdAt: Date };

type Product = { id: number; title: string; price: number };

const keyboard: WithTimestamp<Product> = {
  id: 1,
  title: "Keyboard",
  price: 79.99,
  createdAt: new Date(),
};

console.log(keyboard);
