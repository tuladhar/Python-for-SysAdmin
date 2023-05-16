"""
This is a very simple script that flattens a nested sequence and transforms it from something like this
[1, [2], [[3, "string", [5, 6]], 7], 8] to this [1, 2, 3, "string", 5, 6, 7, 8]
It is recursive generator
"""
from collections import Iterable
def nested_sequence_flattener(nested_sequence: list | tuple, ignored: tuple=(str,bytes)):
    for item in nested_sequence:
        """we check if item is another iterable sequence on inside parent, but only tuple or list because string
        is also an iterable but we do not want it to be flattened (but it is possible)"""
        if isinstance(item, Iterable) and not isinstance(item, ignored):
            yield from nested_sequence_flattener(item, ignored)
        yield item


if __name__ == "__main__":
    seq = [1, [2], [[3, "string", [5, 6]], 7], 8]
    for i in nested_sequence_flattener(seq):
        print(i)

"""
End note:
as an administrator you may come across some really messed up datasets of ie user information. This script has come
in really handy for me sometimes when i got some data to enter to the system in some 'author had no idea what they were
doing'-format 
"""