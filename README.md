# Chalk 1.2
## Simple, easy to learn interpreted programming language.
### Hello world!
`write "Hello world!"`
### Variables
#### Chalk supports integers, strings and boolean data types.
```
github = "dhill0n"
age = 15
likes_coding = true
has_gf = false
```

### If statements
#### Use @variable_name to reference a variable
#### Bug: only the innermost statements blocks are executed!
```
animal = "Cat"
favorite_animal = "Cat"
if @animal == @favorite_animal then
  write "You like cats too huh?"
end if`
```

### For loops
#### Coming soon! 
```
for 0 to 10 as i loop
  write @i
end for
```
