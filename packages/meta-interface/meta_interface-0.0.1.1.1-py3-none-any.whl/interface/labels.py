def abstractmethod(funcobj):
    """A decorator indicating abstract methods.

    Requires that the metaclass is `Interface` or derived from it.  A
    class that has a metaclass derived from `Interface` cannot be
    instantiated unless all of its abstract methods are overridden.
    The abstract methods can be called using any of the normal
    'super' call mechanisms. `abstractmethod(_)` may be used to declare
    abstract methods for properties and descriptors.

    Usage:
        class IBase(Interface[Base]):
            @abstractmethod
            def my_abstract_method(self, ...): pass
        
        class C(metaclass=IBase):
            def my_abstract_method(self, ...):
                print(self)
    
    """
    funcobj.__isabstractmethod__ = True
    return funcobj

def defaultmethod(funcobj):
    """A decorator indicating methods with default implementations.

    Requires that the metaclass is `Interface` or derived from it.  A
    class that has a metaclass derived from `Interface` can be
    instantiated without being overridden.
    The default methods can be called using the class name with `self`
    passed when overriding. `defaultmethod(_)` may be used to declare
    implemented methods for properties and descriptors.

    Usage:

        class IBase(Interface[Base]):
            @defaultmethod
            def my_method(self, ...):
                print(self)
        
        class C(Base, metaclass=IBase):
            def my_method(self, ...):
                IBase.my_method(self, ...)
                print('overriden')
        
    """
    funcobj.__isdefaultmethod__ = True
    return funcobj

def declaredclass(classobj):
    """A decorator indicating the class
    that the restriced interface will be based on.

    Requires that the class is not provided with
    particular definition but need to be referred.

    Usage:
    
        @declaredclass
        class Base: pass
        
        class IBase(Interface[Base]):
            @abstractmethod
            def my_method(self, ...): pass
        
        class Base(metaclass=IBase):
            def my_method(self, ...):
                print(self)
            
    """
    classobj.__isdeclaredclass__ = True
    return classobj