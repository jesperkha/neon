# Neon Language Documentation

> **DISCLAIMER:** None of these features have been added yet since the compiler is not finished. However, all of these features will be present in the final product

## Introduction

Neon is a statically typed compiled language. It is designed to be a more modern version of C, but still keeps control and minimal abstraction. Syntactically it's similar to Go, but many additional features are inspired by languages like Haskell and Rust.

Neon aims to give a better experience when working with lower level data. Additionally, it's easy to port C libraries to Neon. This means you can spend less time re-inventing the wheel and writing long-winded ports for simple libraries, and instead quickly start working alongside a C codebase.

## Installation

Neon is not yet in a state where it can be installed or even run

## Hello World

In a file ending with `.ne` write:

```go
func main() {
    println("hello world!")
}
```

Compile and run by using the command `neon run <filename>`, when done it should print out `hello world` to the terminal. You just successfully created your first Neon program!

In Neon, functions are declared with the `func` keyword followed by their name. The `main` function will be the entry point of your program, similar to most compiled languages. Unlike C, you dont need to return the exit code. On success the program will exit with code `0`, on failure `1`. To specify a custom exit code use the built-in `exit()` function.

The output binary is deleted after running. To keep it, run `neon build <filename>` instead. To just build the C files without compiling, run `neon gen <filename>` (this will create a new directory called `__neon__` and dump the files there).

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

## Comments

```go
// this is a comment
```

## Variables

```go
name := "John"
age  := 32

height: f32 = 1.83
friends: []string = ["Amy", "Carl", "Fred"]
```

When declaring variables using the `:=` operator the variables type is automatically set based on the right hand value. Here `name` will be `string` and `age` will be `int`. Another way to declare variables is to define a type along with it. The type comes after the colon `:` and must match the right hand values type. However, this declaration uses a single equal sign `=` instead.

The `:=` operator will always infer the generic type of the right hand value. For example, any integer will be typed as `int` (`i64`), any float will be typed as `float` (`f64`) etc.

Also notice the difference between declarations and assignment:

```go
a := 0     // declaration with :=
b: int = 0 // declaration with type suffix and =
c = 0      // assignment with =
```

Variables cannot be defined at the global scope (top level). Unused variables and variable shadowing is not recommended and will raise a warning. Warnings do not terminate compilation, but will be printed to the terminal.

## Types

### Primitives

```go
bool

string

char
byte

int // is i64
i8 i16 i32 i64
u8 u16 u32 u64

float // is f64
f32 f64

any
```

### Numbers

Number literals can have different types: `1` is an `int`, but `1.0` is a `float`. Mismatched types are not allowed in expressions, so to fix any type differences you can use casting:

```go
1 + 1.0        // error: mismatched types int and float
float(1) + 1.0 // ok
```

### Strings

Strings are immutable. They act as a fixed array of characters, but they have been abstracted into their own type. This allows for string operations like adding two strings together:

```go
s := "hello, "
john := "John"
println(s + john) // hello, John
```

Strings can also be indexed, the returned type will be `char`:

```go
s := "abc"
println(s[1]) // b
```

`char` literals are written with `''` instead of `""`:

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

You can get the value at an index `i` with `arr[i]`. Negative indexing is also allowed: `arr[-i]` (this is equivalent to `arr[len(arr)-i]`; the last element)

To append elements to an array use the `+` operator. The right hand value can either be a single value of the correct type or another array:

```go
arr := [1, 2]
arr = arr + 3 // append 3
arr += [4, 5] // append 4 and 5
arr = 0 + arr // add 0 to beginning

println(arr) // [0, 1, 2, 3, 4, 5]
```

Arrays have two built-in properties which you can access with the respective function:

- `len(arr: []any)`: *length* of array. The number of elements or the total size if initialized with a length.
- `cap(arr: []any)`: *capacity* of array. The maximum number of elements that can be appended before needing to re-allocate.

> Neon automatically resizes arrays to fit the elements and arrays are always 0 initialized.

All built-in array functions:

- `len()`: returns length of array
- `cap()`: returns capacity of array
- `pop()`: removes and returns the last element
- `clear()`: empties array, does not change the capacity

Neon uses arrays as a replacement to memory pointers. In C you would have to allocate a chunk of memory using `malloc()` for example, but in Neon the `make()` function is used for memory allocation. It is given the type for the array and a size:

```go
// This initializes an array of ints with length 1024
nums := make(int, 1024)
```

## Statements

### If

```go
name := "Carl"

if name == "Carl" {
    println("Hello, Carl!")
} else if name == "John" {
    println("Hello, John!")
} else {
    println("Who are you?")
}
```

The `if` statement is exactly the same as most languages. However, unlike some, it does not need the parenthesies around the expression.

Logical operators:
- `==`: *is equal*
- `!=`: *not equal*
- `&&`: *logical and*
- `||`: *logical or*
- `<`, `>`, `<=`, `>=`: *less than, greater than, less or equal to, greater or equal to*
- `in`: *is member*, checks to see if the left value is a member of the right value:
    ```go
    "dog" in ["cat", "dog", "fox"] // true
    ```
- `is`: *type equality*, checks to see if the left value is of the right type:
    ```go
    123 is int // true
    ```
