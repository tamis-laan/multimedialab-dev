#include <Python.h>
static PyObject* say_hello(PyObject* self, PyObject* args)
{
    const char* name;
    if (!PyArg_ParseTuple(args, "s", &name))
        return NULL;
    printf("Hello %s!\n", name);
    Py_RETURN_NONE;
}

static PyObject* sliding_window(PyObject* self, PyObject* args)
{ 	
	float *name;
	//Get the two input Lists
	PyObject *w;
	PyObject *l;
	if(!PyArg_ParseTuple(args,"OO",&w,&l))
		return NULL;
	
	PyObject *val = PyTuple_GetItem(w,0);
	
	/*	
	int a;
	!PyArg_ParseTuple(w,"d",a);
	printf("value: %d",a);


	//Define itterator to itterate over list ellements
	PyObject *it 	= PyObject_GetIter(w);
	PyObject *witem;

	while(witem=PyIter_Next(it))
	{
		!PyArg_ParseTuple(witem,"f", &name);
		printf("value: %f",*name);
	}
	printf("HELLO PYTHON");
*/

	Py_RETURN_NONE;
}
 
static PyMethodDef WindowMethods[] =
{
     	{"say_hello", say_hello, METH_VARARGS, "Greet somebody."},
	{"sliding_window", sliding_window, METH_VARARGS, "Slide a window over a and b"},
	{NULL, NULL, 0, NULL}
};

 
PyMODINIT_FUNC
 
initwindow(void)
{
     (void) Py_InitModule("window", WindowMethods);
}

