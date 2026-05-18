# Fria
Framework for Real-time Interactive Applications works in requestAnimationFrame(), as opposed to event-driven DOM applications. It is designed to create animated visual applications using the start/update pattern used by e.g Unity, Processing and other real-time engines.

## Getting started
Objects implementing the Updatable interface can be added to UpdateDispatcher singleton.
From then on, they will have their update() method called automatically by UpdateDispatcher upon every requestAnimationFrame().

## Helpers
Fria also includes several useful helper classes/functions that can be used independently:
- **Serialization** Deserialize and serialize typed objects from/to anonymous JSON objects
- **Event Dispatcher** Add custom events to objects, without relying on standard DOM events
- **Geometry** Set of basic geometry classes (Point, Rectangle) for 2D/3D graphics, together with algebraic operations on the structures
- **Tween** Animated interpolation of numbers and Points