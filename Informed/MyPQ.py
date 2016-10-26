# NOTE: Partial implementation taken from python documentation:
# https://docs.python.org/3/library/heapq.html#priority-queue-implementation-notes
import itertools
from heapq import heappush, heappop
class MyPriorityQueue:
    '''Variant of Queue that retrieves open entries in priority order (lowest first).

        Entries are typically tuples of the form:  (priority number, data).
        '''

    def __init__(self, maxsize=None):
        self.queue = []
        self.entry_finder = {}
        self.counter = itertools.count()
        self.qsize = 0

    def add_task(self, task, priority=0):
        'Add a new task or update the priority of an existing task'
        #if task in self.entry_finder:
        #    remove_task(task)
        count = next(self.counter)
        entry = [priority, count, task]
        #convert task (node) to tuple
        tuple_task = tuple(task.path)
        self.entry_finder[tuple_task] = entry
        self.qsize += 1
        heappush(self.queue, entry)

    def pop_task(self):
        'Remove and return the lowest priority task. Raise KeyError if empty.'
        while self.queue:
            priority, count, task = heappop(self.queue)
            #if task is not REMOVED:
            self.qsize -= 1
            tuple_task = tuple(task.path)
            del self.entry_finder[tuple_task]
            return task
        raise KeyError('pop from an empty priority queue')

    def empty(self):
        if self.qsize == 0:
            return True
        else:
            return False

"""
    def _qsize(self):
        return len(self.queue)

    def _put(self, item):
        heappush(self.queue, item)

    def _get(self):
        return heappop(self.queue)
"""