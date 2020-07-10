from enum import Enum
from tempfile import NamedTemporaryFile

import graphviz
import networkx

from . import config as cfg
from . import events


class EventState(Enum):
    asleep = 1
    awake = 2
    success = 3
    failure = 4


class Event:
    def __init__(self, name, condition):
        self.name = name
        self.condition = condition
        self.precondition = AllBefore()
        self.outcome = AllAfter()
        self.state = EventState.asleep
        self.wake_time = 0

    def __repr__(self):
        return self.name

    def reset(self):
        self.state = EventState.asleep
        self.wake_time = 0

    def update(self, time, verbose=False):
        if self.state is EventState.asleep:
            if self.precondition is None or self.precondition():
                self.state = EventState.awake
                self.wake_time = time
                if verbose:
                    print("{} is waiting to happen.".format(self))
        if self.state is EventState.awake:
            if self.condition():
                self.state = EventState.success
                if verbose:
                    print("{} has happened.".format(self))
                if self.outcome:
                    self.outcome(self.condition)
            elif time - self.wake_time > cfg.MAX_WAIT_TIME:
                self.state = EventState.failure
                if verbose:
                    print("{} has not happened.".format(self))

    @property
    def failure(self):
        return self.state is EventState.failure

    @property
    def success(self):
        return self.state is EventState.success


class Transition:
    def __init__(self, source=None, dest=None):
        self.source = source
        self.dest = dest
        self.active = False

    def __repr__(self):
        r = "transition from {} to {}".format(self.source, self.dest)
        return r


class AnyBefore:
    """Precondition"""
    def __init__(self, transitions=None):
        self.transitions = transitions if transitions is not None else []

    def __call__(self):
        return any(trans.active for trans in self.transitions)


class AllBefore:
    """Precondition"""
    def __init__(self, transitions=None):
        self.transitions = transitions if transitions is not None else []

    def __call__(self):
        # Also works on the root node since all([]) == True :)
        return all(trans.active for trans in self.transitions)


class AllAfter:
    """Outcome"""
    def __init__(self, transitions=None):
        self.transitions = transitions if transitions is not None else []

    def __call__(self, condition):
        for trans in self.transitions:
            trans.active = True


class CategoricalAfter:
    """Outcome"""
    def __init__(self, transitions=None, categories=None, verbose=False):
        self.transitions = transitions if transitions is not None else []
        self.categories = categories if categories is not None else []
        self.verbose = verbose

    def __call__(self, condition):
        category = condition()
        for trans, c in zip(self.transitions, self.categories):
            if c == category:
                trans.active = True
                if self.verbose:
                    print("Activating {}.".format(trans))


class CausalGraphState:
    success = 1
    failure = 2


class CausalGraphTraverser:
    def __init__(self, root, verbose=False):
        self.root = root
        self.verbose = verbose
        self.state = None
        # This is a legacy attribute to work with old termination conditions.
        self.last_wake_time = 0

    def get_event(self, name):
        to_traverse = {self.root}
        traversed = set()
        while to_traverse:
            event = to_traverse.pop()
            if event.name == name:
                return event
            if event.outcome:
                for trans in event.outcome.transitions:
                    if trans.dest not in traversed:
                        to_traverse.add(trans.dest)
            traversed.add(event)
        return None

    def get_events(self):
        to_traverse = {self.root}
        traversed = []
        while to_traverse:
            event = to_traverse.pop()
            if event.outcome:
                for trans in event.outcome.transitions:
                    if trans.dest not in traversed:
                        to_traverse.add(trans.dest)
            traversed.append(event)
        return traversed

    def get_successful_events(self):
        return [e for e in self.get_events() if e.success]

    def reset(self):
        self.state = None
        self.last_wake_time = 0
        to_reset = {self.root}
        reset = set()
        while to_reset:
            event = to_reset.pop()
            event.reset()
            if event.outcome:
                for trans in event.outcome.transitions:
                    trans.active = False
                    if trans.dest not in reset:
                        to_reset.add(trans.dest)
            reset.add(event)

    def update(self, time):
        if self.state in (CausalGraphState.success, CausalGraphState.failure):
            return
        failed = False
        awake = False
        to_process = {self.root}
        while to_process:
            event = to_process.pop()
            event.update(time, verbose=self.verbose)
            if event.state is EventState.success and event.outcome:
                for trans in event.outcome.transitions:
                    if trans.active:
                        to_process.add(trans.dest)
            elif event.state is EventState.failure:
                failed = True
            elif event.state is EventState.awake:
                awake = True
                # Legacy
                self.last_wake_time = max(event.wake_time, self.last_wake_time)
        if not awake:
            if failed:
                self.state = CausalGraphState.failure
                if self.verbose:
                    print("Failure of {} with {}".format(self, event))
            else:
                self.state = CausalGraphState.success
                if self.verbose:
                    print("Success of {} with {}".format(self, event))
        return not self.terminated

    @property
    def success(self):
        return self.state is CausalGraphState.success

    @property
    def terminated(self):
        return self.state in (CausalGraphState.success,
                              CausalGraphState.failure)


class CausalGraphViewer:
    def __init__(self, root):
        self.root = root
        self._file = NamedTemporaryFile()
        self.colors = {
            EventState.asleep: 'white',
            EventState.awake: 'yellow',
            EventState.success: 'green',
            EventState.failure: 'orange',
        }

    def render(self, filename=None, compact=True):
        filename = filename if filename else self._file.name
        g = graphviz.Digraph('G', filename=filename)
        g.attr('node', shape='circle')
        g.attr('node', fontname='Linux Biolinum O')
        to_process = {self.root}
        processed = set()
        if compact:
            self._labels = {}
            label = 'A'
            for event in CausalGraphTraverser(self.root).get_events():
                self._labels[event.name] = label
                label = increment_str(label)
        while to_process:
            event = to_process.pop()
            if event in processed:
                continue
            node_label = self._labels[event.name] if compact else event.name
            g.node(node_label, style='filled', color='black',
                   fillcolor=self.colors[event.state])
            if event.outcome:
                for trans in event.outcome.transitions:
                    edge_label = None if compact else str(int(trans.active))
                    dest_label = (self._labels[trans.dest.name] if compact
                                  else trans.dest.name)
                    g.edge(node_label, dest_label, label=edge_label)
                    to_process.add(trans.dest)
            processed.add(event)
        g.view()


def connect(source, dest):
    """Connect two events.

    source.outcome and dest.precondition must exist.

    """
    trans = Transition(source, dest)
    source.outcome.transitions.append(trans)
    dest.precondition.transitions.append(trans)


def increment_char(c):
    """Increment an uppercase character, returning 'A' if 'Z' is given."""
    return chr(ord(c) + 1) if c != 'Z' else 'A'


def increment_str(s):
    lpart = s.rstrip('Z')
    num_replacements = len(s) - len(lpart)
    new_s = lpart[:-1] + increment_char(lpart[-1]) if lpart else 'A'
    new_s += 'A' * num_replacements
    return new_s


def load_causal_graph(graph_data):
    g = networkx.DiGraph()
    if not graph_data:
        return g
    # First pass for the nodes
    for event_data in graph_data:
        event = getattr(events, event_data['type'])
        g.add_node(event_data['name'], event=event, args=event_data['args'])
    # Second pass for the edges
    for event_data in graph_data:
        name = event_data['name']
        try:
            children = event_data['children']
        except KeyError:
            children = []
        for child in children:
            g.add_edge(name, child)
    # Find the root
    g.graph['root'] = next(n for n, d in g.in_degree() if d == 0)
    return g


def embed_event(scene, name, event_type, **event_kwargs):
    kw = event_kwargs.copy()
    for key, value in kw.items():
        if type(value) is str:
            path = scene.graph.find("**/" + value + "_solid")
            if not path.is_empty():
                kw[key] = path
    if events.needs_world(event_type):
        kw['world'] = scene.world
    return Event(name, event_type(**kw))


def embed_causal_graph(causal_graph, scene, verbose=True):
    if not len(causal_graph):
        return None
    events = {name: embed_event(scene, name, data['event'], **data['args'])
              for name, data in causal_graph.nodes.data()}
    for parent, child in causal_graph.edges:
        connect(events[parent], events[child])
    root = events[causal_graph.graph['root']]
    embedded_causal_graph = CausalGraphTraverser(root=root, verbose=verbose)
    return embedded_causal_graph
