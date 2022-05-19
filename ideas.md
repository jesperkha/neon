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

<br>

## `using` statement

```go
// Lets say you have a long function that does a lot of
// calculations with a lot of variables:
func foo() {
    ...

    a := 1
    b := "hello"
    c := int[1, 2, 3]

    // Instead of extracting some lines of code into another function
    // which will only be used here, you can instead create a new scope
    // that only has access to the variables you want to include:
    using a, b {
        print a // 1
        print b // hello
        print c // error: c is not defined
    }

    // You can also output a value, however this means you have to specify
    // the type of the variable. You cannot use the using statement for
    // reassignment or return
    d: int = using a {
        return a + 1
    }
}
```

<br>

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

print sum // 4
```

<br>

## Keeping function state

```go
// Lets say you have a function that needs to keep some state, for
// this example we will just implement an iterator function.

// In other languages you would need to either have some global
// variables to access or even use a class. However, this is where
// the 'st' keyword comes in play:
func next_person(): string {
    // You can define local variables that will keep their values
    // between function calls by using the 'st' (store) prefix
    st idx := 0

    person := people[idx]
    idx++
    return person
}

people := string["John", "Amy", "Carl"]

print next_person(people) // John
print next_person(people) // Amy
print next_person(people) // Carl
```
