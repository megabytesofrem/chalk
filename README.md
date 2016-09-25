# Chalk 1.5
Simple, easy to learn interpreted programming language.

Chalk is dynamic, and typeless which means it infers from what you enter.

Here are some basic examples of Chalk programming.

More can be found in the /tests/ folder.
### Hello world!
`write "Hello world!"`
### Variables
Chalk supports integers, strings and boolean data types.
```
github = "dhill0n"
age = 15
likes_coding = true
has_gf = false
```

### If statements
Compare two values or variables and execute some code if they do or don't match
```
animal = "Cat"
favorite_animal = "Cat"
if @animal == @favorite_animal {
  write "You like cats too huh?"
}
```

### For loops
Repeat blocks of code as many times as you want
```
for x in 0 .. 10 {
  write @x
}
```

### While Loops
Repeat blocks of code while a condition is or isn't met
```
-- Will never ever be false! :D
while @likes_coding == true {
  write "Coding is amazing!"
}
```

### Functions
Group blocks of code for easy access and less repetition.
```
func greet (user) {
  write "Hello @user"
}

greet ("@github")
```
