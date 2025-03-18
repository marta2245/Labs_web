from abc import ABC, abstractmethod

# 1. Породжувальний патерн — Factory Method
class Animal(ABC):
    @abstractmethod
    def speak(self):
        pass

class Dog(Animal):
    def speak(self):
        return "Woof!"

class Cat(Animal):
    def speak(self):
        return "Meow!"

class AnimalFactory:
    @staticmethod
    def get_animal(animal_type):
        if animal_type == "dog":
            return Dog()
        elif animal_type == "cat":
            return Cat()
        else:
            raise ValueError("Unknown animal type")

# Використання фабричного методу
animal = AnimalFactory.get_animal("dog")
print(animal.speak())  # Woof!


# 2. Структурний патерн — Adapter
class EuropeanPlug:
    def provide_electricity(self):
        return "220V"

class USPlug:
    def provide_power(self):
        return "110V"

class Adapter:
    def __init__(self, plug):
        self.plug = plug

    def provide_electricity(self):
        if isinstance(self.plug, USPlug):
            return "Converted to 220V"
        return self.plug.provide_electricity()

# Використання адаптера
us_plug = USPlug()
adapter = Adapter(us_plug)
print(adapter.provide_electricity())  # Converted to 220V


# 3. Поведінковий патерн — Observer
class Subject:
    def __init__(self):
        self._observers = []

    def attach(self, observer):
        self._observers.append(observer)

    def detach(self, observer):
        self._observers.remove(observer)

    def notify(self, message):
        for observer in self._observers:
            observer.update(message)

class Observer(ABC):
    @abstractmethod
    def update(self, message):
        pass

class ConcreteObserver(Observer):
    def __init__(self, name):
        self.name = name

    def update(self, message):
        print(f"{self.name} received: {message}")

# Використання спостерігача
subject = Subject()
observer1 = ConcreteObserver("Observer 1")
observer2 = ConcreteObserver("Observer 2")

subject.attach(observer1)
subject.attach(observer2)

subject.notify("Update available!")
# Observer 1 received: Update available!
# Observer 2 received: Update available!
