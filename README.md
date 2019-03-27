# Chalk (archive)
An old project from 2016/2017 started by my friend Dhillon. This is an archive but if you would like to start this project back up then feel free to contribute and I will follow suit.

Simple, easy to learn interpreted programming language written in Python 3.

Chalk is dynamic, and typeless which means it infers from what you enter.

## Contributing
Feel free to contribute, please be descriptive in the pull request.

## Usage

More can be found in the /tests/ folder or on the wiki.

### Hello world!
`write "Hello world!"`

### Variables
Chalk supports integers, strings and boolean data types.

More data types will be added in the future like Lists and Dictionaries.
```
github = "dhill0n"
age = 15
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
