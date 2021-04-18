#include "chalk.h"

PyObject *py_module;
PyObject *py_module_dict;
PyObject *py_parser_class_item;

PyObject *py_chalk_err_unknown;
PyObject *py_chalk_err_syntax;
PyObject *py_chalk_err_parser;
PyObject *py_chalk_err_undefined_variable;
PyObject *py_chalk_err_undefined_statement;

int chalk_init() {
	Py_Initialize();
	
	PyObject *sys = PyImport_ImportModule("sys");
	PyObject *path = PyObject_GetAttrString(sys, "path");
	PyList_Append(path, PyUnicode_FromString("."));
	
	PyObject *py_module_str = PyUnicode_FromString("chalkc");
	py_module = PyImport_Import(py_module_str);
	Py_DECREF(py_module_str);
	if (!py_module) {
		PyErr_Print();
		return 1;
	}
	
	py_module_dict = PyModule_GetDict(py_module);	
	py_parser_class_item = PyDict_GetItemString(py_module_dict, "Parser");
	
	py_chalk_err_undefined_variable = PyDict_GetItemString(py_module_dict, "ChalkUndefinedVariable");
	
	py_chalk_err_unknown = PyDict_GetItemString(py_module_dict, "ChalkUnknownError");
	py_chalk_err_syntax = PyDict_GetItemString(py_module_dict, "ChalkSyntaxError");
	py_chalk_err_parser = PyDict_GetItemString(py_module_dict, "ChalkParserError");
	py_chalk_err_undefined_variable = PyDict_GetItemString(py_module_dict, "ChalkUndefinedVariable");
	py_chalk_err_undefined_statement = PyDict_GetItemString(py_module_dict, "ChalkUndefinedStatement");

	return 0;
}


int chalk_free(py_chalk_t *chalk) {
	Py_DECREF(py_module);
	Py_DECREF(chalk->py_parser_class);
	
	return 0;
}

int chalk_new(py_chalk_t *chalk) {
	chalk->py_parser_class = PyObject_CallObject(py_parser_class_item, NULL);
	
	return 0;
}

int chalk_deinit() {
	Py_DECREF(py_module);
	Py_DECREF(py_module_dict);
	Py_DECREF(py_parser_class_item);

	return 0;
}

void chalk_free_output(char ***out, size_t len) {
	for (size_t i = 0; i < len; i++) {
		free(*out[i]);
	}
	free(*out);
	*out = NULL;
}

int chalk_parse_line(py_chalk_t *chalk, char *line, char ***out, size_t *out_len) {
	PyObject *value = PyObject_CallMethod(chalk->py_parser_class, "parse", "(s)", line);
	if (PyErr_Occurred()) {
		int err_code = 0;
		PyObject *type, *value, *traceback;
		PyErr_Fetch(&type, &value, &traceback);
		PyObject *value_pystr = PyObject_Str(value);
		PyObject *encoded_value_str = PyUnicode_AsEncodedString(value_pystr, "UTF-8", "strict");
		char *value_str = PyBytes_AS_STRING(encoded_value_str);
		Py_DECREF(encoded_value_str);
		Py_DECREF(value_pystr);
		
		if (PyErr_GivenExceptionMatches(type, py_chalk_err_syntax)) {
			err_code = CHALK_ERROR_SYNTAX;
		} else if (PyErr_GivenExceptionMatches(type, py_chalk_err_parser)) {
			err_code = CHALK_ERROR_PARSER;
		} else if (PyErr_GivenExceptionMatches(type, py_chalk_err_undefined_variable)) {
			err_code = CHALK_ERROR_UNDEFINED_VARIABLE;
		} else if (PyErr_GivenExceptionMatches(type, py_chalk_err_undefined_statement)) {
			err_code = CHALK_ERROR_UNDEFINED_STATEMENT;
		} else {
			err_code = CHALK_ERROR_UNKNOWN;
		}
		
		Py_DECREF(type);
		Py_DECREF(value);
		Py_DECREF(traceback);
		
		size_t value_str_len = strlen(value_str) + 1;
		*out = malloc(sizeof(char *));
		*out[0] = malloc(sizeof(char) * value_str_len);
		strncpy(*out[0], value_str, value_str_len);
		*out_len = 1;
		
		return err_code;
	} else if (PyList_Check(value)) {
		Py_ssize_t buffer_len = PyList_Size(value);
		*out = malloc(sizeof(char *) * buffer_len);
		
		for (int i = 0; i < buffer_len; i++) {
			PyObject *item = PyList_GetItem(value, i);
			PyObject *item_str = PyObject_Str(item);
			PyObject *encoded_line_str = PyUnicode_AsEncodedString(item_str, "utf-8", "strict");
			char *line_str = PyBytes_AS_STRING(encoded_line_str);
			Py_DECREF(encoded_line_str);
			size_t line_str_len = strlen(line_str) + 1;
			*out[i] = malloc(sizeof(char) * line_str_len);
			strncpy(*out[i], line_str, line_str_len);
		}
		*out_len = buffer_len;
		return 0;
	} else {
		out = NULL;
		*out_len = 0;
		return CHALK_ERROR_UNKNOWN;
	}
}