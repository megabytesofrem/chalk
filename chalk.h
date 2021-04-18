#ifndef CHALK_H
#define CHALK_H

#include <stdio.h>
#include "Python.h"

struct py_chalk_t {
	PyObject *py_parser_class;
} typedef py_chalk_t;

enum chalk_error {
	CHALK_ERROR_UNKNOWN = 1,
	CHALK_ERROR_SYNTAX = 2,
	CHALK_ERROR_PARSER = 3,
	CHALK_ERROR_UNDEFINED_VARIABLE = 4,
	CHALK_ERROR_UNDEFINED_STATEMENT = 5,
};

int chalk_init();
int chalk_free(py_chalk_t *chalk);
int chalk_new(py_chalk_t *chalk);
int chalk_deinit();
void chalk_free_output(char ***out, size_t len);
int chalk_parse_line(py_chalk_t *chalk, char *line, char ***out, size_t *out_len);

#endif