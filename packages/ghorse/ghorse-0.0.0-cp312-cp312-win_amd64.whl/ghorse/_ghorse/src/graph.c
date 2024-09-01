#include "ghorse/graph.h"

PyObject *
GraphObject_new(PyTypeObject *type, PyObject *args, PyObject *kwds)
{
    GraphObject *self;
    self = (GraphObject *) type->tp_alloc(type, 0);
    return (PyObject *) self;
}

int
GraphObject_init(GraphObject *self, PyObject *args, PyObject *kwds)
{
    // TODO: implement
    self->node_count = 0;
    return 0;
}

void
GraphObject_dealloc(GraphObject *self)
{
    Py_TYPE(self)->tp_free((PyObject *) self);
}

PyObject *
GraphObject_number_of_nodes(GraphObject *self, PyObject *Py_UNUSED(ignored))
{
    return PyLong_FromSize_t(self->node_count);
}
