import weakref


class Interface(type):
    """
    Metaclass for defining an interface.

    Use this metaclass to create an interface. An interface should be subclassed
    directly, and then acts as a mix-in class. It restricts the classes which
    observe this interface, and those classes should implement the abstract methods
    declared in the interface and can call the methods with default implementations.
    
    Usage:
        class IC(Interface):
            @abstractmethod
            def my_abstract_method(self, ...): pass
        
        class C(metaclass=IC):
            def my_abstract_method(self, ...):
                print(self)
    
    Furthermore, if the interface should only be observed by a certain class or its
    subclasses, which means that the interface can call the methods defined in that
    certain class, the only things that should be changed is just from `Interface`
    to `Interface[AnyClass]`.
    
    Usage:
        class IBase(Interface[Base]):
            @abstractmethod
            def my_abstract_method(self, ...): pass
        
        class C(Base, metaclass=IBase):
            def my_abstract_method(self, ...):
                print(self)
    """
    
    def __new__(*args, **kwargs):
        raise TypeError('`Interface` should be specified by its subclass.')
    
    def __new_subclass__(mcls, name, bases, namespace, /, **kwargs):
        cls = super().__new__(mcls, name, bases, namespace, **kwargs)
        dirs = dir(mcls)
        for name in dirs:
            _iter_in_dirs(name, mcls, cls)
        return cls
    
    def __init_subclass__(cls):
        cls.__new__ = Interface.__new_subclass__
        return super().__init_subclass__()
    
    @classmethod
    def __class_getitem__(cls, typename):
        restricted_interface = _restricted_interfaces.get(typename)
        if restricted_interface is None:
            
            class RestrictedInterface(type):
                def __new__(*args, **kwargs):
                    raise TypeError('`Interface` should be specified by its subclass.')
                
                def __new_subclass__(mcls, current_name, bases, namespace, /, **kwargs):
                    cls = super().__new__(mcls, current_name, bases, namespace, **kwargs)
                    if current_name == typename.__name__ and getattr(typename, "__isdeclaredclass__", False):
                        _restricted_interfaces.pop(typename)
                        this_typename = cls
                        _restricted_interfaces[this_typename] = RestrictedInterface
                    else:
                        this_typename = typename
                    if issubclass(cls, this_typename) or (cls is this_typename):
                        dirs = dir(mcls)
                        for name in dirs:
                            _iter_in_dirs(name, mcls, cls)
                        return cls
                    else:
                        raise TypeError(str(cls) + ' should be the subclass of ' + str(this_typename) + '.')
                
                def __init_subclass__(cls):
                    cls.__new__ = RestrictedInterface.__new_subclass__
                    return super().__init_subclass__()

            restricted_interface = RestrictedInterface
            _restricted_interfaces[typename] = restricted_interface
        return restricted_interface


class Interfaces:
    """
    Metaclass for defining multiple interfaces.

    Use this metaclass to create multiple interfaces. When it is necessary to observe many
    interfaces, use this metaclass. It initializes in the order of the interface arguments.
    For example, if multiple interfaces all have a method with a same name, and the class that
    observes those interfaces will apply only the method of the final one.
    
    Usage:
        class IC(Interface):
            @abstractmethod
            def my_abstract_methodA(self, ...): pass
        
        class IBase(Interface[Base]):
            @abstractmethod
            def my_abstract_methodB(self, ...): pass
        
        class C(Base, metaclass=Interfaces(IC, IBase)):
            def my_abstract_methodA(self, ...):
                print(self, 'A')
            
            def my_abstract_methodB(self, ...):
                print(self, 'B')
    """
    def __new__(cls, *args, **kwargs):
        class Interfaces(*args, *kwargs.values()): pass
        return Interfaces


_restricted_interfaces = weakref.WeakValueDictionary()


def _iter_in_dirs(name, mcls, cls):
    current = getattr(mcls, name, None)
    if current is not None:
        cls_attr = getattr(cls, name, None)
        if getattr(current, "__isabstractmethod__", False):
            if (cls_attr is None) or (cls_attr.__code__ == current.__code__):
                raise TypeError('Function `' + name + '` has not been implemented.')
        elif getattr(current, "__isdefaultmethod__", False):
            if (cls_attr is None) or (cls_attr.__code__ == current.__code__) or (len(cls_attr.__code__.co_names) == 0 and len(current.__code__.co_names) != 0):
                setattr(cls, name, current)