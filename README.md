# Chalk
Simple, easy to learn interpreted programming language written in Python 3.

Chalk is dynamic, and typeless which means it infers from what you enter.

## Contributing
Feel free to contribute, please be descriptive in the pull request.

We also have a Telegram chat to discuss changes and the future direction of the language. Check it out [here](https://telegram.me/joinchat/EHl7-UEEO0TzENj0oAxz0Q).

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
