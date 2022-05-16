# Types

```c
// int by default is a 64 bit signed integer, but you can specify size and
// if its signed or not with the extra type below
int
i8, i16, i32, i64
u8, u16, u32, u64

// float is a 64 bit floating point number
float
f32, f64

string
char
byte
bool
```

```go
// For arrays you define the type after brackets []

[]int     // Arrays of integers
[5]string // 5 element long array of strings

// When using values like numbers in expressions, depending on how you write them
// they can give different types

a := 5   // a is int
b := 3.1 // b is float

// Neon is strict when is comes to type checking and will not allow mixing floats
// and ints. The following expression will raise a compile-time error because it
// is mixing a float (1.0) and an int (1)
1.0 + 1

// Neons type order is the same as Go. It is readable and makes intuituive sense:
[10]*string
// "length 10 array of pointers to string"
```
