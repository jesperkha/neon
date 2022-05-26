# Language feature ideas

## Bit masking

```js
// Gets the bits in specified range. Returned type is the same as the original
num: u8 = ...
first4 := num[4 <-]   // gets the 4 first bits (from the right)
last4  := num[-> 4]   // gets the 4 last bits (from the left)
middle := num[2 -> 4] // gets the 4 next bits starting at index 2

// You can also specify a type to convert to
two_chars: u16 = ...
a := num[char]    // gets the 8 first bits (length of char), a is now of type char
b := num[char ->] // gets the 8 last bits
```

## `using` statement

```go
// Lets say you have a long function that does a lot of
// calculations with a lot of variables:
func foo() {
    a := 1
    b := "hello"
    c := [1, 2, 3]

    // Instead of extracting some lines of code into another function
    // which will only be used here, you can instead create a new scope
    // that only has access to the variables you want to include:
    using a, b {
        println(a) // 1
        println(b) // hello
        println(c) // error: c is not defined
    }

    // You can also output a value, however this means you have to specify
    // the type of the variable. You cannot use the using statement for
    // reassignment or return
    d: int = using a {
        return a + 1
    }
}
```

## Haskells `where` syntax

```go
// Abstract an expression into symbolic representations with 'where'
sum := a + b where {
    a := 1
    b := 2

    // You can also define helper values etc
    c := 3
    b = c
}

println(sum) // 4
```

## Keeping function state

```go
// Lets say you have a function that needs to keep some state, for
// this example we will just implement an iterator function.

// In other languages you would need to either have some global
// variables to access or even use a class. However, this is where
// the 'st' keyword comes in play:
func next_person(p: []string): string {
    // You can define local variables that will keep their values
    // between function calls by using the 'store' prefix
    store idx := 0

    person := p[idx]
    idx += 1
    return person
}

func main() {
    people := ["John", "Amy", "Carl"]
    
    println(next_person(people)) // John
    println(next_person(people)) // Amy
    println(next_person(people)) // Carl
}
```

## Built-in functions

```go
print(s: string)   // printlns string out to stdout
println(s: string) // Same as println() but with a newline at the end
error(s: string)   // printlns s out to stderr and exits with code 1
exit(c: int)	   // Halts execution and exits with code c

// Returns an array of t with length l. t cannot be an array type
// Used as memory allocation. TYPE represents a type name (int, string etc)
make(t: TYPE, l: int)

len(arr: []any) // Returns length of array arr
cap(arr: []any) // Returns cap of array arr
```

## Macros

Have som macros predefined which will be inserted at compilation. They can even be reflective like the line number and filename:

```go
func main() {
    num_args  := len($args)
    prog_name := $args[0]
    cur_line  := $line
    filename  := $filename
}
```

Turns into:

```go
func main() {
    num_args  := len(["main.exe", "some", "args"])
    prog_name := ["main.exe", "some", "args"][0]
    cur_line  := 4
    filename  := "main.ne"
}
```

## Defer

```go
func foo() {
    file := openfile(...)
    defer close(file) // Will push this action to the bottom of the function

    ...

    // close() is executed here
}
```