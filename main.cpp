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
        Py_DECREF(pConstruct);
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
    void match(){
        const char* res;
        PyObject* pMatch = PyObject_CallMethod(pIns,"match",NULL);
//        if(pMatch==NULL) printf("return null");
//        else printf("return success!");
//        PyArg_ParseTuple(pMatch,"s",&res);
//        printf("%s\n",res);
    }
//    void match(){
//        PyObject_CallMethod(pIns,"match",NULL);
//    }
    ~DDPG(){
        Py_DECREF(pModule);
        Py_DECREF(pDict);
        Py_DECREF(pAgent);
        Py_DECREF(pIns);
//        cout << "DDPG Agent deconstrction completed!" << endl;
    }
};


int main() {
    DDPG agent = DDPG();
    agent.get_s0();
    agent.get_a0();
//    string new_file = agent.match();
    agent.match();
    return 0;
}
