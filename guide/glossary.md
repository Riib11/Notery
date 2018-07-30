# Glossary

Documentation for all built-in command words in Notery

<!-------------------------------------------------------------->
## Notation

- Command Word: A special word that must be prefixed by `\` in order to be referenced.
- Constant: An immutable value that is set once - when it is bound.
- Function: A function is set once, but must be evaluated (with the approprate arguments) as an individual instance for each reference, sensative to the execution context.
- `$`: prefix for function argument names.

<!-------------------------------------------------------------->
## Constants

<!-------------------------------------------------------------->
## Functions

### Fundamentals

##### let $name $type
Define a new constant `$name`. Tag `$name` to indicate to the compiler that `$name` must be later `set` to have a value with the type `$type`.

##### set $name $value
If `$name` is undefined, then define a new constant `$name`. Bind `$name` to `$value`.

##### function $name $arg_1 ... $arg_n $result
Define a new function `$name` that takes the arguments `$arg_1`, ...,`$arg_n`. When invoked, `$name` reduces to `$result` which can refer to the arguments as temporarily defined constants.

##### module $name $child_1 ... $child_n
Define a new module `$name` with the children `$child_1`, ..., `$child_n`

<!-------------------------------------------------------------->
### Utilities

##### repeat $times $content
Reduces to `$body` repeated `$times` times.

##### loop $times $command
Reduces to `times` number of invocations of `$command`.

