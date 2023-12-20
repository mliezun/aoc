from collections import defaultdict
from abc import ABC


modules = """broadcaster -> a, b, c
%a -> b
%b -> c
%c -> inv
&inv -> a"""

modules = """broadcaster -> a
%a -> inv, con
&inv -> b
%b -> con
&con -> output"""

modules = open("input.txt", "r").read().strip()

modules = [m.split(" -> ") for m in modules.splitlines() if m.strip()]

ITERATIONS = 0
OUT_PULSES = defaultdict(list)


class Module(ABC):
    def __init__(self, name: str):
        self.name = name
        self.outputs = []

    def receive_pulse(self, mod: "Module", pulse: int) -> list[tuple["Module", int]]:
        # print(f"{mod and mod.name} -{pulse}-> {self.name}")
        return self.process_pulse(mod, pulse)

    def connect_output(self, mod: "Module"):
        self.outputs.append(mod)

    def propagate_pulse(self, pulse: int):
        mods = []
        for m in self.outputs:
            mods.append((m, pulse))
        return mods

    def process_pulse(self, mod: "Module", pulse: int):
        raise NotImplementedError()

    def __str__(self) -> str:
        return f"{self.__class__.__name__}(name={self.name})"

    def __repr__(self) -> str:
        return str(self)


class TestModule(Module):
    def process_pulse(self, mod: "Module", pulse: int):
        return []


class Broadcaster(Module):
    def process_pulse(self, mod: "Module", pulse: int):
        return super().propagate_pulse(pulse)


class FlipFlop(Module):
    def __init__(self, name: str):
        super().__init__(name)
        self.state = 0

    def process_pulse(self, mod: "Module", pulse: int):
        if pulse == 0:
            self.state = (self.state + 1) % 2
            return super().propagate_pulse(self.state)
        return []


class Conjunction(Module):
    def __init__(self, name: str):
        super().__init__(name)
        self.memory = {}

    def remember_input(self, mod: Module):
        self.memory[mod.name] = 0

    def start_recording(self):
        self.recording = []

    def record(self, pulse: int):
        if hasattr(self, "recording"):
            if pulse:
                OUT_PULSES[self.name].append((ITERATIONS, len(self.recording)))
                # print(self.name, "it=",ITERATIONS, "len=",len(self.recording))
            self.recording.append(pulse)

    def process_pulse(self, mod: Module, pulse: int):
        self.memory[mod.name] = pulse
        if all(self.memory.values()):
            self.record(0)
            return self.propagate_pulse(0)
        self.record(1)
        return self.propagate_pulse(1)


def parse_modules(modules: list) -> dict[str, Module]:
    modules_by_name = {}
    outputs_by_name = {}
    for m in modules:
        module_type = m[0]
        module_outputs = [o.strip() for o in m[1].split(",") if o.strip()]
        if module_type.startswith("broadcaster"):
            modules_by_name[module_type] = Broadcaster(module_type)
            outputs_by_name[module_type] = module_outputs
        elif module_type.startswith("%"):
            modules_by_name[module_type[1:]] = FlipFlop(module_type[1:])
            outputs_by_name[module_type[1:]] = module_outputs
        elif module_type.startswith("&"):
            modules_by_name[module_type[1:]] = Conjunction(module_type[1:])
            outputs_by_name[module_type[1:]] = module_outputs
    for name, outputs in outputs_by_name.items():
        for mod_name in outputs:
            mod = modules_by_name.get(mod_name, TestModule(mod_name))
            modules_by_name[name].connect_output(mod)
            if isinstance(mod, Conjunction):
                mod.remember_input(modules_by_name[name])
    return modules_by_name


def push_button(modules_by_name: dict[str, Module]):
    broad = modules_by_name["broadcaster"]
    queue = [(broad, broad.receive_pulse(None, 0))]
    while queue:
        current, signals = queue.pop(0)
        for mod, pulse in signals:
            queue.append((mod, mod.receive_pulse(current, pulse)))


modules = parse_modules(modules)
lv = modules["lv"]
lv_inputs = [modules[k] for k in lv.memory.keys()]
for m in lv_inputs:
    m.start_recording()

for i in range(100_000):
    ITERATIONS += 1
    push_button(modules)

accum = 1
for name, pulses in OUT_PULSES.items():
    accum *= pulses[0][0]
print("result:", accum)
