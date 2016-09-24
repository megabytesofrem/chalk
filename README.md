# Chalk 1.4
Simple, easy to learn interpreted programming language.
### Hello world!
`write "Hello world!"
### Variables
Chalk supports integers, strings and boolean data types.
```
github = "dhill0n"
age = 15
likes_coding = true
has_gf = false
```

### If statements
Use @variable_name to reference a variable.
```
animal = "Cat"
favorite_animal = "Cat"
if @animal == @favorite_animal then
  write "You like cats too huh?"
end if`
```

### For loops
Loop through ranges and store the count in a variable. 
```
for x in 0 .. 10 do
  write @x
end for
```

### While Loops
Loop while a condition is not met.
```
-- Will never ever be false! :D
while @likes_coding == true do
  write "Coding is amazing!"
end while
```

### Functions
Geoup common code together for easy use
```
func greet(user) {
  write "Hello @user"
}

greet("@github")
```
