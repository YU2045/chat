import flet as ft
from typing import TypeVar, Generic, Callable

T = TypeVar('T')


class State(Generic[T]):

    def __init__(self, value: T):
        self._value = value
        self._observers: list[Callable] = []

    def get(self):
        return self._value

    def set(self, new_value: T):
        if self._value != new_value:
            self._value = new_value
            for observer in self._observers:
                observer()

    def bind(self, observer):
        self._observers.append(observer)


class ReactiveState(Generic[T]):
    def __init__(self, formula: Callable[[], T], reliance_states: list[State]):
        self.__value = State(formula())
        self.__formula = formula
        self._observers: list[Callable] = []

        for state in reliance_states:
            state.bind(lambda _: self.update())

    def get(self):
        return self.__value.get()

    def update(self):
        old_value = self.__value.get()
        self.__value.set(self.__formula())

        if old_value != self.__value.get():
            for observer in self._observers:
                observer()

    def bind(self, observer):
        self._observers.append(observer)


StateProperty = T | State[T] | ReactiveState[T]


def bind_props(props: list[StateProperty], bind_func: Callable[[], None]):
    for prop in props:
        if isinstance(prop, State) or isinstance(prop, ReactiveState):
            prop.bind(lambda _: bind_func())


def get_prop_value(prop: StateProperty):
    if isinstance(prop, State):
        return prop.get()
    elif isinstance(prop, ReactiveState):
        return prop.get()
    else:
        return prop


class ReactiveText(ft.UserControl):
    def __init__(self, text: StateProperty[str], size: StateProperty[int] = 17):
        super().__init__()
        self.control = ft.Text('')
        self.text = text
        self.size = size
        self.set_props()

        if isinstance(self.text, State):
            self.text.bind(lambda _: self.update())
        if isinstance(self.size, State):
            self.size.bind(lambda _: self.update())

    def set_props(self):
        if isinstance(self.text, State):
            self.control.value = self.text.get()
        else:
            self.control.value = self.text

        if isinstance(self.size, State):
            self.control.size = self.size.get()
        else:
            self.control.size = self.size

    def update(self):
        self.set_props()
        self.control.update()

    def build(self):
        return self.control
