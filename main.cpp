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
        PyRun_SimpleString("import os");
        PyRun_SimpleString("sys.path.append('/home/tangsong/CLionProjects/InvokeDDPGtest/tbcnn-terminal')");
        this->pModule = PyImport_ImportModule("DDPG"); // import "DDPG"
        this->pDict = PyModule_GetDict(pModule); // import the method in "DDPG"
        this->pAgent = PyDict_GetItemString(pDict,"DDPG"); // pAgent stores the python class "DDPG
        PyObject* pConstruct = PyInstanceMethod_New(pAgent); // constructor of DDPG
        // DDPG object pIns
        this->pIns = PyObject_CallObject(pConstruct,NULL);// an instance of DDPG
//        cout << "DDPG Agent constrction completed!" << endl;
//        Py_Finalize();
    }
    void get_s0(){
        PyObject* ps0 = PyObject_CallMethod(pIns,"get_s0",NULL);
//        PyObject* ps0 = PyObject_CallMethod(pIns,"get_s0","s",Py_BuildValue("s","/home/tangsong/CLionProjects/InvokeDDPGtest/test.js"));
    }
    void get_a0(){
        PyObject* pa0 = PyObject_CallMethod(pIns,"select_action",NULL);
//        PyObject* ps0 = PyObject_CallMethod(pIns,"get_s0","s",Py_BuildValue("s","/home/tangsong/CLionProjects/InvokeDDPGtest/test.js"));
    }
    ~DDPG(){
//        cout << "DDPG Agent deconstrction completed!" << endl;
    }
};


int main() {
    DDPG agent = DDPG();
    agent.get_s0();
    agent.get_a0();
//    Py_Initialize();
//    PyRun_SimpleString("import sys");
//    PyRun_SimpleString("import os");
//    PyRun_SimpleString("sys.path.append('/home/tangsong/CLionProjects/InvokeDDPGtest/tbcnn-terminal')");
//    PyObject *rM = PyImport_ImportModule("restore_model");
//    if(!rM) printf("rm not found");
//    PyObject *rMm = PyModule_GetDict(rM);
//    PyObject *f2v = PyDict_GetItemString(rMm,"fileString_convert_vector");
//    if(!f2v) printf("method not found");
//    PyObject_CallFunction(f2v,"s","/home/tangsong/CLionProjects/InvokeDDPGtest/test.js");
//    Py_Finalize();
    return 0;
}
