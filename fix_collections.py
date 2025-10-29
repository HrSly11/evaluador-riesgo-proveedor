"""
Parche para hacer experta compatible con Python 3.10+
Debe importarse ANTES de importar experta
"""
import collections
import collections.abc

# Parche para compatibilidad con Python 3.10+
for name in dir(collections.abc):
    if not hasattr(collections, name):
        setattr(collections, name, getattr(collections.abc, name))

# Específicamente para frozendict
if not hasattr(collections, 'Mapping'):
    collections.Mapping = collections.abc.Mapping
if not hasattr(collections, 'MutableMapping'):
    collections.MutableMapping = collections.abc.MutableMapping
if not hasattr(collections, 'Iterable'):
    collections.Iterable = collections.abc.Iterable
if not hasattr(collections, 'MutableSet'):
    collections.MutableSet = collections.abc.MutableSet