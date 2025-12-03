/********************
 * Modified from the file execute_python.h of
 * Olivier Parcollet's project: execute_python.
 * See https://github.com/parcollet/execute_python
 * ******************/

// states the interpreter
// extern "C" int init_python_interpreter(const char* python_so);
int init_python_interpreter(const char* python_so);

// // executes code in the interpreter
int execute_python_file(const char* filename);
//
// // call only ONCE at the very end !
int close_python_interpreter();
