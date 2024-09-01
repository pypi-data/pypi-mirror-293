#ifndef GHORSE_GHORSE_GRAPH_H_
#define GHORSE_GHORSE_GRAPH_H_

#include <Python.h>

typedef struct {
    PyObject_HEAD
    size_t node_count;
} GraphObject;

PyObject *GraphObject_new(PyTypeObject *type, PyObject *args, PyObject *kwds);
int       GraphObject_init(GraphObject *self, PyObject *args, PyObject *kwds);
void      GraphObject_dealloc(GraphObject *self);

PyObject *GraphObject_number_of_nodes(GraphObject *self,
                                      PyObject    *Py_UNUSED(ignored));

PyDoc_STRVAR(AdjacencyList_doc, "Representation of graph via adjacency list.");

#endif  // GHORSE_GHORSE_GRAPH_H_
