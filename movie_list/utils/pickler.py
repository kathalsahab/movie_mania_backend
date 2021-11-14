"""This utility file contains wrapper methods for Pickle functions
"""
import pickle


def dump(obj):
    """This method is used to dump an Object and get back pickled Byte response

    Args:
        obj (Object): Object to be dumped

    Returns:
        [Bytes]: [The dumped response]
    """
    try:
        return pickle.dumps(obj)
    except pickle.PickleError as pickle_error:
        raise pickle.PickleError(pickle_error)


def load(obj):
    """This method is used to load an Byte object and get back pickled Object response

    Args:
        obj (Bytes): Byte object to be loaded

    Returns:
        [Object]: [Loaded response]
    """
    try:
        return pickle.loads(obj)
    except pickle.PickleError as pickle_error:
        raise pickle.PickleError(pickle_error)
