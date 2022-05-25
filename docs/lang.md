# Neon Language Documentation

> **DISCLAIMER:** None of these features have been added yet since the compiler is not finished, however, all of these features will be present in the final product

## Hello World

In a file ending with `.ne` write:

```go
func main() {
    println("hello world!")
}
```

Compile and run by using the command `neon run <filename>`, when done it should print out `hello world` to the terminal. You just successfully created your first Neon program!

In Neon, functions are declared with the `func` keyword followed by their name. The `main` function will be the entry point of your program, similar to most compiled languages. Unlike C, you dont need to return the exit code. On success the program will exit with code `0`, on failure `1`. To specify a custum exit code use the built-in `exit()` function.

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

When declaring variables using the `:=` operator the variables type is automatically set based on the right hand value. Here `name` will be `string` and `age` will be `int`. You can also specify the type after a colon `:`.

The `:=` operator will always infer the generic type of the right hand value. For example, any integer will be typed as `int` (`i64`), any float will be typed as `float` (`f64`) etc.

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
1 + 1.0      // error: mismatched types int and float
f64(1) + 1.0 // ok since float is f64
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
```

Arrays can only hold one type, which is defined either by the variable definition or the first element of the array. You can use casting to define a more specific type of array:

```go
[u16(0), 0, 0] // Array literal of u16s
```

You can get the value at an index `i` with `arr[i]`. Negative indexing is also allowed: `arr[-i]` (this is equivalent to `arr[len(arr)-i]`; the last element)

To append elements to an array use the `+` operator. The right hand value can either be a single value of the correct type or another array:

```go
arr := [1, 2]
arr = arr + 3
arr += [4, 5]

println(arr) // [1, 2, 3, 4, 5]
```

Arrays have two built-in properties which you can access with the respective function:

- `len(arr: []any)`: *length* of array. The number of elements or the total size if initialized with a length.
- `cap(arr: []any)`: *capacity* of array. The maximum number of elements that can be appended before needing to re-allocate.

> Neon automatically resizes arrays to fit the elements and arrays are always 0 initialized.

Neon uses arrays as a replacement to memory pointers. In C you would have to allocate a chunk of memory using `malloc()` for example. However, in Neon the `make()` function is used for memory allocation. It is given the type for the array and a size:

```go
// This initializes an array of ints with length 1024
nums := make(int, 1024)
```

All built-in array functions:

- `len()`: returns length of array
- `cap()`: returns capacity of array
- `pop()`: removes and returns the last element
- `clear()`: empties array, does not change the capacity
