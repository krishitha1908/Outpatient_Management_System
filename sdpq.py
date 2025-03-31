class Queue:
    def __init__(self):
        self.items = []

    def enqueue(self, item):
        self.items.append(item)

    def dequeue(self):
        if not self.is_empty():
            return self.items.pop(0)
        else:
            return None
        
    def front(self):
        if not self.is_empty():
            return self.items[0]
        else:
            return None

    def is_empty(self):
        return len(self.items) == 0

    def size(self):
        return len(self.items)

aqueue = Queue()

def penqueue(aqueue,patient_id):
    aqueue.enqueue(patient_id)
    return True

def pdequeue(aqueue):
    return aqueue.dequeue()

def front(aqueue):
    return aqueue.front()