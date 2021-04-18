#include <stdio.h>
#include "chalk.h"

int main() {
	chalk_init();
	
	py_chalk_t chalk;
	chalk_new(&chalk);
	
	char *chalk_line = "write \"chalk in c\"";
	
	int chalk_error;
	char **out = NULL;
	size_t out_len = 0;
	if ((chalk_error = chalk_parse_line(&chalk, chalk_line, &out, &out_len)) == 0) {
	    printf("out len: %ld\n", out_len);
		printf("chalk output:\n");
		if (out != NULL) {
			for (size_t i = 0; i < out_len; i++) {
				printf("%s\n", out[i]);
			}
		} else {
			printf("(empty output)\n");
		}
	} else {
		printf("[chalk error] ");
		switch (chalk_error) {
			case CHALK_ERROR_UNKNOWN:
				printf("unknown");
				break;
			case CHALK_ERROR_SYNTAX:
				printf("syntax error");
				break;
			case CHALK_ERROR_PARSER:
				printf("parser error");
				break;
			case CHALK_ERROR_UNDEFINED_VARIABLE:
				printf("undefined variable");
				break;
			case CHALK_ERROR_UNDEFINED_STATEMENT:
				printf("undefined statement");
				break;
			default:
				printf("undocumented error");
	}
		printf(": %s\n", out[0]);	
	}
	chalk_free_output(&out, out_len);
	
	chalk_free(&chalk);
	chalk_deinit();
	
	return 0;
}