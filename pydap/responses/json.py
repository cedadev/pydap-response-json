import itertools
from simplejson import dumps

import numpy

from pydap.model import *
from pydap.lib import INDENT, encode_atom, walk
from pydap.responses.dds import dispatch as dds_dispatch
from pydap.responses.lib import BaseResponse


class JSONResponse(BaseResponse):
    def __init__(self, dataset):
        BaseResponse.__init__(self, dataset)
        self.headers.append(('Content-type', 'application/json'))

    @staticmethod
    def serialize(dataset):
        attributes = {}
        for child in walk(dataset):
            attributes[child.id] = child.attributes
        if hasattr(dataset, 'close'): dataset.close()
        return [dumps(attributes)]


def dispatch(var, printname=True):
    dispatchers = [(SequenceType, _sequence),
                   (StructureType, _structure),
                   (BaseType, _base)]

    for klass, func in dispatchers:
        if isinstance(var, klass):
            return func(var, printname)


def _structure(var, printname):
    for child in var.walk():
        for line in dispatch(child, printname):
            yield line
        yield '\n'


def _sequence(var, printname):
    yield ', '.join(child.id for child in var.values())
    yield '\n'
    for struct_ in var:
        out = []
        for child in struct_:
            for line in dispatch(child, printname=False):
                out.append(line)
        out = ', '.join(out).split('\n')
        for line in out:
            if line:
                yield line.strip(', ') + '\n'


def _base(var, printname):
    if printname:
        yield var.id
        yield '\n'

    data = numpy.asarray(var.data).flat
    if var.shape:
        for indexes, value in itertools.izip(numpy.ndindex(var.shape), data):
            index = '[%s]' % ']['.join(str(idx) for idx in indexes)
            yield '%s %s\n' % (index, encode_atom(value))
    else:
        yield encode_atom(var.data)
