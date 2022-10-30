# Chalk (archive)

Simple, easy to learn interpreted programming language written in Python 3.

Chalk is dynamic, and typeless which means it infers from what you enter.

## A message from 2021

5 years later and wiser, me and Alice feel the same way about Chalk as how historians feel when studying the pyramids. We don't understand how despite the bad code quality and severe lack of experience that some parts, like if statements, work well. Chalk has only stuck around because against all odds a project from when we knew very little turned out cool. It feels like a monkey and a typewriter situation.

I've added C bindings to the Python class so I could add it to a chat bot written in another language, at least now the c at the end of `chalkc.py` resembles reality. Details about the C bindings are listed below.

## Usage
`python3 chalkc.py [file]`

## Syntax

### Hello world!
`write "Hello world!"`

### Variables
Chalk supports integers, strings and boolean data types.

More data types will be added in the future like Lists and Dictionaries.
```
language = "chalkc"
features = 2
```

### Functions
Chalk supports the ability to define functions.

Functions can be called with the following syntax: `timestable(10)`

```
func timestable (n) {
  for table in 0 .. @n {
    res = n * n
    write "@n*@n = @res"
  }
}

timestable (10)
```

## Contributing
Feel free to contribute, please be descriptive in the pull request.

## C Bindings

C bindings are optional and only present here to add the original Chalk interpreter to another project.

C documentation can be found in `C.md`. There is an included example program (`example.c`) to demonstrate how to use and build a program using Chalk.

### Building and Installing the Library (Mac)

1. Install Python 3 from Homebrew with `brew install python3`
2. Check which Python version your using with `python3 --version` and make note of the major and minor, e.g. Python 3.9.2 would become 3.9.
3. In the `Makefile` change the Python version at "`LIBS =`" (for Darwin) from `-lpython3.9` to the version you just installed.
4. Install the Python Chalk package using pip with `pip3 install .`.
5. Run `make` to build the library.
6. Run `sudo make install` to install to `/usr/local/`. Use the environment variable `PREFIX` for an alternate installation path.

### Building and Installing the Library (Linux)

1. Install the Python 3 development package for your distribution (`python3-dev` on Ubuntu, `python3` on Arch) and `pip3`.
2. Install the Python Chalk package using pip with `pip3 install .`.
3. Run `make` to build the library.
4. Run `sudo make install` to install to `/usr/local/`. Use the environment variable `PREFIX` for an alternate installation path.

### Example C App

Once you have configured the environment as listed above you can run `make example` to build and run an example app, it's a simple implementation that parses a single line and prints the output/any errors that may occur. Take a look at `example.c` for the code.

### Python Path

I want to make a note that the step "`pip3 install .`" listed above is important to make the library portable on your system. Because the C bindings are just tapping into a Python file it's obviously required to be present, by installing the file to Python's `site-packages` it means that `chalkc.py` doesn't need to be in the working directory at runtime.

If you want to hack around with a custom `chalkc.py` using the C bindings, I've added the working directory to Python's path at runtime. This means if you `pip3 uninstall chalkc` and keep the modified Python file in your working directory at runtime it'll use the custom version and doesn't require the pip package. It's not recommended for anything more than hacking as you lose all portability.
