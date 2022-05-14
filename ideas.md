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