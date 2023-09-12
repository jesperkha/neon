# Neon Language Documentation

> **DISCLAIMER:** None of these features have been added yet since the compiler is not finished. However, all of these features will be present in the final product

## Introduction

Neon is a statically typed compiled language. It is designed to be a more modern version of C, but still keeps control and minimal abstraction. Syntactically it's similar to Go, but many additional features are inspired by languages like Haskell and Rust.

Neon aims to give a better experience when working with lower level data. Additionally, it's easy to port C libraries to Neon. This means you can spend less time re-inventing the wheel and writing long-winded ports for simple libraries, and instead quickly start working alongside a C codebase.

<br>

## Installation

> Installation is not yet available

<br>

## Hello World

Create a file called `main.ne` and write:

```go
func main() {
    println("hello world!")
}
```

Compile and run with `neon run <filename>`, when done it should print out `hello world!` to the terminal. You just successfully created your first Neon program!

In Neon, functions are declared with the `func` keyword followed by their name. The `main` function will be the entry point of your program, similar to most compiled languages. There can only be one main function. Unlike C, you dont need to return the exit code. On success the program will exit with code `0`, on failure `1`. To specify a custom exit code use the built-in `exit()` function.

By default, Neon builds and runs the binary in a temporary directory. To build the binary in the current directory run `neon build <filename>`. To just tanspile to C without compiling, run `neon gen <filename>`. By default this will dump the files in a new `neon_src` directory, but you can specify the output directory with the `-dir` flag.

<br>

## Project structure

A Neon project consists of several modules, with each module being its own directory (except the top level module, also called the main module). The modules are automatically named after their directories and can be imported like this:

```
main.ne
other/
    hello.ne
```

```go
import "other"

func main() {
    other.say_hello()
}
```

<br>

## Comments

```go
// this is a comment
```

<br>

## Variables

```go
// Automatically infer the type
name := "John"
age  := 32

// Specify type
height: f32 = 1.83
friends: []string = ["Amy", "Carl", "Fred"]
```

When declaring variables using the `:=` operator the variables type is automatically set based on the right hand value. In the example above, `name` will be `string` and `age` will be `int`. Another way to declare variables is to put the type after a colon `:`. The user given type and the type of the right hand expression must match.

The `:=` operator will always infer the "basic" type of the right hand value. For example, any integer will be typed as `int` and any float will be typed as `float`.

Also notice the difference between declarations and assignment:

```go
a := 0     // declaration with :=
b: int = 0 // declaration with type suffix and =
c = 0      // assignment with =
```

Variables cannot be defined at the global scope. Unused variables and variable shadowing is not recommended and will raise a warning. Warnings do not terminate compilation, but will be printed to the terminal if not disabled (enabled by default).

<br>

## Types

### Primitives

```go
bool

string

char
byte

int // is i32
i8 i16 i32 i64
u8 u16 u32 u64

float // is f32
f32 f64

any // is only used in builtin functions
```

### Numbers

Number literals can have different types: `1` is an `int`, but `1.0` is a `float`. Mismatched types are not allowed in expressions, so to fix any type differences you can use casting:

```go
1 + 1.0        // error: mismatched types int and float
float(1) + 1.0 // ok
```

### Strings

Strings have been abstracted into their own type, but act as an array of `char`. You can add two strings with the `+` operator:

```go
hello := "Hello, "
john  := "John"
println(hello + john) // Hello, John
```

Strings can also be indexed, the returned type will be `char`:

```go
s := "abc"
println(s[1]) // b
```

`char` literals are written with single quotes `''` instead of double quotes `""`. A `char` literal cannot contain more than one character.

```go
c: char = 'a'
```

### Arrays

```go
a := [1, 2, 3]
b: []char = ['a', 'b', 'c']

// This is not allowed since the compiler wont
// know which type the array contains
c := []
```

Arrays can only hold one type, which is defined either by the variable definition or the first element of the array. You can use casting to define a more specific type of array:

```go
[u16(0), 0, 0] // Array literal of u16
```

You can get the value at an index `i` with `arr[i]`. Negative indexing is also allowed: `arr[-i]` (this is equivalent to `arr[len(arr)-i]`. This will not work if it goes below `0`).

To append elements to an array use the `+` operator. The right hand value can either be a single value of the correct type or another array:

```go
arr := [1, 2]
arr = arr + 3 // append 3
arr += [4, 5] // append 4 and 5
arr = 0 + arr // add 0 to beginning

println(arr) // [0, 1, 2, 3, 4, 5]
```

Arrays have two built-in properties which you can access with the respective functions:

- `len(arr: []any)`: _length_ of array. The number of elements or the total size if initialized with a length.
- `cap(arr: []any)`: _capacity_ of array. The maximum number of elements that can be appended before needing to re-allocate.

> Neon automatically resizes arrays to fit the elements and arrays are always 0-initialized.

All built-in array functions:

- `len()`: returns length of array
- `cap()`: returns capacity of array
- `pop()`: removes and returns the last element
- `clear()`: empties array, does not change the capacity

<br>

## Memory

Neon uses arrays as an abstraction to memory pointers. Use the `alloc()` function to allocate a chunk of memory on the heap. It takes the type of the array and a size:

```go
// This initializes an array of ints with length 1024
nums := alloc(int, 1024)
```

Neon automatically puts values on the heap if they are passed to another scope:

```go
func foo() {
    a := "A" // stack
    b := "B" // heap

    c := [1, 2, 3] // stack
    d := [4, 5, 6] // heap

    bar(b, d)
}

func bar(str: string, arr: []int) {
    ...
}
```

But dont worry, Neon also automatically frees this memory when it is no longer in use!

To ensure that no out-of-bounds memory is read or written to, Neon tries to lint index errors at compile time. In cases where that's not possible, Neon adds runtime error handlers (with cleanup) in the generated code.

<br>

## Control flow and logic
