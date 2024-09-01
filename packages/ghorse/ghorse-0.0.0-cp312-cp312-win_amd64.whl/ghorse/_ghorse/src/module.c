#include <Python.h>

#include "ghorse/freeze.h"
#include "ghorse/graph.h"

static PyMethodDef GhorseMethods[] = {
    {"freeze", ghorse_freeze, METH_FASTCALL,
     "Modify graph to prevent further change by adding or removing nodes or "
     "edges."},
    {NULL, NULL, 0, NULL},
};

static PyMethodDef GraphObject_methods[] = {
    {"number_of_nodes", (PyCFunction) GraphObject_number_of_nodes, METH_NOARGS,
     "Returns the number of nodes in the graph."},
    {NULL},
};

static PyTypeObject GraphType = {
    /* clang-format off */
    .ob_base = PyVarObject_HEAD_INIT(NULL, 0)
    .tp_name = "ghorse._ghorse.Graph",
    /* clang-format on */
    .tp_doc = PyDoc_STR("Base class for undirected graphs."),
    .tp_basicsize = sizeof(GraphObject),
    .tp_itemsize = 0,
    .tp_flags = Py_TPFLAGS_DEFAULT | Py_TPFLAGS_BASETYPE,
    .tp_new = GraphObject_new,
    .tp_init = (initproc) GraphObject_init,
    .tp_dealloc = (destructor) GraphObject_dealloc,
    .tp_methods = GraphObject_methods,
};

PyDoc_STRVAR(ghorse_doc, "ghorse._ghorse: Internal C implementation.");

static struct PyModuleDef ghorsemodule = {
    PyModuleDef_HEAD_INIT, "_ghorse", ghorse_doc, -1, GhorseMethods,
};

PyMODINIT_FUNC
PyInit__ghorse(void)
{
    PyObject *module;
    if (PyType_Ready(&GraphType) < 0)
        return NULL;

    module = PyModule_Create(&ghorsemodule);
    if (module == NULL)
        return NULL;

    if (PyModule_AddObjectRef(module, "Graph", (PyObject *) &GraphType) < 0) {
        Py_DECREF(module);
        return NULL;
    }

    return module;
}
