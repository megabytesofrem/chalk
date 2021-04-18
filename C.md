# C Binding Documentation

The Chalk interpreter is a Python program so to run Chalk under C the library uses the Python runtime library. The library works by creating a Chalk instance (`py_chalk_t`) and then passing it to methods to mutate state and get runtime output. A Chalk instance must always be freed when no longer needed.

## Linking notes

Checkout `README.md` for building and installing instructions.

## Important setup and cleanup

`chalk_init()` must be called once before using the library, if you have initialized you must call `chalk_deinit()` before exiting. This is different to creating and freeing Chalk instances, these must each only be called only once throughout the program's lifetime when using the library.

```
chalk_init();

// ... using chalk ...

chalk_deinit();
```

## Creating a Chalk instance

Create an empty struct and then pass it's reference to `chalk_new`.

```
py_chalk_t chalk;
chalk_new(&chalk);
```

## Freeing a Chalk instance

Once you no longer need the instance or need to reset its state, you pass the reference of a previously created Chalk instance to `chalk_free`.

```
py_chalk_t chalk;
chalk_new(&chalk);

// ... using the instance ...

chalk_free(&chalk);
```

## Parsing Chalk lines

Because of the nature of the interpreter, you must parse each line separately and then check for any output or errors. `chalk_parse_line` takes a Chalk instance, the line string to parse, the reference to a `char *` array and a reference to a `size_t` to list how many lines the output is. Each item in the referenced array represents a line of standard output. The method returns 0 on success, or an integer form of a `chalk_error`. Upon error the standard output array may contain a user readable error at the first entry, make sure to check that output length contains more items than 0 before accessing it.

You are responsible for the memory allocation of the standard output array after parsing a line. You should free it after you no longer need it with `chalk_free_output`, you must pass a reference to the array and how long it is.

```
char *chalk_line = "write \"chalk in c\"";

int chalk_error;

char **out = NULL;
size_t out_len = 0;

if ((chalk_error = chalk_parse_line(&chalk, chalk_line, &out, &out_len)) == 0) {
	printf("chalk output:\n");
	if (out != NULL) {
		for (int i = 0; i < out_len; i++) {
				printf("%s\n", out[i]);
		}
	} else {
		printf("(empty output)\n");
	}
} else {
	printf("chalk error code: %d\n", chalk_error);	
	if (out != NULL && out_len > 0) {
	    printf("chalk error description: %s\n", out[0]);
	}
}

chalk_free_output(&out, out_len);
```

## Errors

Alongside an error code the standard output may also contain a more detailed description.

|Code|Name|Description|
|-|-|-|
|1|`CHALK_ERROR_UNKNOWN`|An unknown error occurred.|
|2|`CHALK_ERROR_SYNTAX`|Invalid syntax was given to the parser.|
|3|`CHALK_ERROR_PARSER`|An error occurred while parsing.|
|4|`CHALK_ERROR_UNDEFINED_VARIABLE`|An undefined variable was used.|
|5|`CHALK_ERROR_UNDEFINED_STATEMENT`|An undefined function was used.|