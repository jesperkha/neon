# Statements

## Print

The built-in `print` statement lets you print out formatted values. Structs and arrays will be printed in a readable format.

```go
names: []int = {"John", "Amy", "Carl"}
print names // ["John", "Amy", "Carl"]
```

<br>

## Function

You can declare a function using the `func` keyword. Return type is specified at the end with a colon `:`, can also return nothing. Use `return` to return a value.

```go
func sum(a: int, b: int): int {
    return a + b
}

func say_hello() {
    print "Hello there!"
}
```

<br>

## Struct

Neons structs are similar to most languages inmplementation. When you define a struct it becomes a local type for that file.

```go
struct person {
    name: string
    age:  int
}

john := person(name: "John", age: 32)
print john.name // John
```

<br>

##
