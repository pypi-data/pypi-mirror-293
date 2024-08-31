# Python Metaclass Based Interface

This is a tiny project that introduces the interface concept to Python.

This documentation describes the use of Python metaclasses to create and manage interfaces in Python. The code defines two primary metaclasses, `Interface` and `Interfaces`, which can be used to enforce interface implementation and manage multiple interfaces respectively.

### Usage

To use this package, it is necessary to import the package firstly. You can import partly, but it will import all here for presentation.

```python
from interface import *
```

## Metaclass `Interface`

The `Interface` metaclass is used to define an interface, which is a way to ensure that certain methods are implemented by any class that claims to implement the interface. This is akin to creating a contract for class behavior.

### Usage

To define an interface using `Interface`, simply declare a class with methods decorated by `@abstractmethod`. Here's a basic example:

```python
class IC(Interface):
    @abstractmethod
    def my_abstract_method(self, ...):
        pass
```

Classes that want to implement this interface should use the interface as a metaclass and provide concrete implementations of all abstract methods:

```python
class C(metaclass=IC):
    def my_abstract_method(self, ...):
        print("Implementation of abstract method")
```

## Restricted Interface

If you want the interface to be specifically implemented by certain classes or their subclasses, the interface can be parameterized by passing a class reference to `Interface`. For example:

### Usage

```python
class IBase(Interface[Base]):
    @abstractmethod
    def my_abstract_method(self, ...):
        pass

class C(Base, metaclass=IBase):
    def my_abstract_method(self, ...):
        print("Restricted implementation")
```

## Metaclass `Interfaces`

The `Interfaces` metaclass allows a class to observe multiple interfaces. Specially, if multiple interfaces define a method with the same name, the implementation in the class observing these interfaces will apply the method from the last interface specified.

### Usage

Here’s how you can use `Interfaces` to make a class observe multiple interfaces:

```python
class IC(Interface):
    @abstractmethod
    def my_abstract_methodA(self, ...): pass

class IBase(Interface[Base]):
    @abstractmethod
    def my_abstract_methodB(self, ...): pass

class C(Base, metaclass=Interfaces(IC, IBase)):
    def my_abstract_methodA(self, ...):
        print('A')
    
    def my_abstract_methodB(self, ...):
        print('B')
```

# Decorators for Interfaces

This documentation provides details on the usage of decorators `abstractmethod`, `defaultmethod`, and `declaredclass` in Python, designed to work with metaclasses derived from `Interface`. These decorators help in defining interface constraints and behaviors for classes.

## Decorator `abstractmethod`

The `abstractmethod` decorator is used to mark methods as abstract within an interface. This indicates that any concrete class implementing this interface must provide an implementation for these methods. 

### Usage

To use `abstractmethod`, include it in a class that uses an `Interface` as its metaclass or is derived from such an interface:

```python
class IBase(Interface[Base]):
    @abstractmethod
    def my_abstract_method(self, ...):
        pass

class C(metaclass=IBase):
    def my_abstract_method(self, ...):
        print("Implemented method")
```

## Decorator `defaultmethod`

The `defaultmethod` decorator indicates that a method has a default implementation within an interface. Classes using this interface can override these methods, but it's not mandatory for instantiation.

### Usage

Here's how to apply `defaultmethod` in your class definitions:

```python
class IBase(Interface[Base]):
    @defaultmethod
    def my_method(self, ...):
        print("Default implementation")

class C(Base, metaclass=IBase):
    def my_method(self, ...):
        IBase.my_method(self, ...)  # Call the default implementation
        print("Overridden implementation")
```

## Decorator `declaredclass`

The `declaredclass` decorator is used to indicate a base class for which an interface wil be specifically restricted. This decorator is essential when an interface is tightly coupled with a specific class.

### Usage

Use `declaredclass` to mark a class as the base class for an interface:

```python
@declaredclass
class Base: pass

class IBase(Interface[Base]):
    @abstractmethod
    def my_method(self, ...):
        pass

class Base(metaclass=IBase):
    def my_method(self, ...):
        print("Method implementation")
```

# Additional Notes

- The `Interface` and `Interfaces` metaclasses include mechanisms to ensure that classes properly implement required methods, either through direct implementation or through class hierarchy constraints.
- The use of these metaclasses makes it clear at the class definition level which interfaces a class intends to implement, promoting better structure and organization in complex systems.
- These decorators require that the class definition includes an appropriate metaclass, either `Interface` or a derivation.
- `abstractmethod` and `defaultmethod` provide a clear indication of method requirements and implementations at the interface level, promoting more robust object-oriented design.
- `declaredclass` ensures the interface is adhered to by a specific class, facilitating controlled implementations and dependencies.

This setup in Python facilitates clear, modular, and maintainable code, especially useful in large projects where enforcing design patterns and consistency is crucial.