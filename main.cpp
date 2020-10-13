#include <iostream>
#include </usr/include/python3.6/Python.h>

using namespace std;

class DDPG{
public:
    PyObject *pModule; // python module
    PyObject *pDict; // python method dictionary in pModule
    PyObject *pAgent; //python class "DDPG" declared in DDPG.py
    PyObject *pIns; // an instance of DDPG
    DDPG(){ // constructor
        Py_Initialize(); // turn on python virtual env
        PyRun_SimpleString("import sys");
        PyRun_SimpleString("sys.path.append('/home/tangsong/CLionProjects/InvokeDDPGtest')");
        this->pModule = PyImport_ImportModule("DDPG"); // import "DDPG"
        this->pDict = PyModule_GetDict(pModule); // import the method in "DDPG"
        this->pAgent = PyDict_GetItemString(pDict,"DDPG"); // pAgent stores the python class "DDPG
        PyObject* pConstruct = PyInstanceMethod_New(pAgent); // constructor of DDPG
//        this->pIns = PyObject_CallObject(pConstruct,NULL);// an instance of DDPG
        cout << "DDPG Agent constrction completed!" << endl;
        Py_Finalize();
    }
    ~DDPG(){
//        cout << "DDPG A./rungent deconstrction completed!" << endl;
    }
};
int main() {
//    DDPG agent = DDPG();
    Py_Initialize();
    PyRun_SimpleString("import sys");
    PyRun_SimpleString("sys.path.append('/home/tangsong/Projects/tbcnn_-master')");
    PyObject *rM = PyImport_ImportModule("sampleJS");
//    PyObject *rMm = PyModule_GetDict(rM);
//    PyObject *f2v = PyDict_GetItemString(rMm,"fileString_convert_vector");
//    PyObject_CallFunction(f2v,"s","/home/tangsong/CLionProjects/InvokeDDPGtest/tbcnn_-master/test.js");
    Py_Finalize();
    return 0;
}
