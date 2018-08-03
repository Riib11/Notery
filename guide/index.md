# Notery - The Guide

## Goals

Notery's goals are to implement the following into a LaTex-like program:

- __Modularity__ of packages, Linux-philosophy style; each package can easily do something small that interacts with everything else modularly and in a straighforward manner (less conflicting package issues like in LaTex!).
- __Customizability__ of each and every thing about a document's resulting appearance, without having to mess with endless built-in and undecypherable parameters.
- __Scripting__ at any scale of complexity; easy to write in quickly and easy to seperate into a package of its own.
- __Copypasterino-Friendly__ via not having endless reserved characters! Don't you just have the arbitraryness of the reserved characters in LaTex? I mean, sometimes being able to type a `^` rather than perhaps a `\^` can feel like a neat feature, but overall its really just restrictive especially when it comes to the others like `[], {}, &, %, etc.` Notery has just one reserved character, the familiar `\`.

## Syntax Basics

There are two types of strings you can write in a notery file:

- Command strings: start with a `\`.
- Normal strings: start with anything else.

The totality of reserved normal-contex characters are: `\`, `|`, and `~`. So you don't have to worry about a bunch of reserved characters! `\` prefixes command words, `|` seperates command invocation arguments, and `~` creates command word references

In the command word context (the name of the command word), the only reserved characters are: `.`,`*`, and, of course, ` `. The `.` character allows access to the children of modules, `*` creates comments. Also, a command word in the form `\.<name>` is interpretted as a function invocation, whereas a command word in the form `\<name>` is interpretted as a constant or variable.

Remember that `\n`s and ` `s are ignored by the lexer in terms of text placement, so you'll need to use certain commands to get special seperations if you want them.

## Compilation

Compiling a notery document consists of the following steps:

1. Read in strings in input file.
2. Compile all command definitions, lazily.
3. Construct document specifications using axiomatic commands (such as document size and orientation and etc). 
4. Use beta-reduction rules on command invocations to simplify the document contents to notery structures.
5. Produce target output type from notery structured document.

In short, the compiler defines all the command words, and then repeatedly uses beta-reduction until there are no command words left to simplify.

## Defining a Document

## Types

There are 5 simple datatypes in Notery: string, bool, int, nat, and float. Text is interpretted as string by default, but to reference a numberic value, use the commands `\.S`, `\.B`, `\.I`, `\.N`, `\.F` for string boolean, integer, natural and float respectively, argumented with the string representation of that value. The type for a reference to a command word is `~\.`. Invoking this command word works a little differently than the other types; basically, `\. x \\` results in `\.x`.

There are three types of command words: functions, constants, and variables. Functions are always prefixed by `\.`. Constants and variables technically act differently, but they are both prefixed by only `\`, without the `.`. Constants exists in the global context, whereas variables are set by function invocations and exist within the local context of the function.

## Invoking Functions

A very simple function invocation looks like `\.let | $name | $value \\`. This command allows you to set the value of a constant. The syntax of commands, put simply, is this:

- Function name starts with `\.`. Following the function name is the function invocation block.
- Function arguments are each prefixed by a `|`, (except for the first argument, where the `|` may be omitted if you like the aethstetic).
- Function invocation blocks are ended by ended by a `\\`

So, if you want to invoke a function `f` that has 2 arguments, write

    \.f | \1 | \2 \\

If you want to invoke a function inside of another function, do

    \.f | \.f \1 | \2 \\ | \.f \3 | \4 \\ \\

which may look hard to read at first, but looks better with some indentations:

    \.f
        | \.f \1 | \2 \\
        | \.f \3 | \4 \\
    \\

super clean! As a side not, syntax highlighting helps a lot.

## Defining new Commands

To define new command words, you have a few options:

##### set

    \.set \name | \value \\

Assigns `$value` to the value of a constant with the name `$name`. These constants are immutable. If a constant of the name `$name` isn't already defined (by the way of `\.let`), then this command defines it.

##### let

    \.let \type \\

Defines a new constant, and indicates that the constant must later be `\set` to a value with the type `$type`.

##### function

    \.function \name | \1 | \2 | ... | \result \\

Defines a new function with the name `\name` that takes arguments `\1`, `\2`, etc. These argument names serve for being referenced in `\result`. When the function is invoked, it is reduced to `\result`, which may include references to the arguments to the function. References to these names look just like references to any other defined command word. The `\.function` arguments are intrepretted with these rules: the first argument is the name of the function, the last argument is the result of the function, any arguments non-inclusevly between the first and last are argument names.

Note: Recursive function definitions are __NOT__ supported, sorry. Maybe that will be added to the language at some point.

## Function Arguments

So as you've noticed there are very simple types, only 5, in Notery. You'll mostly be working with strings, but its useful to have the others as well. Sometimes, you might want a functions arguments to have the right types. Conveniently, Notery organizes strings into arrays automatically, so even though a function argument cannot have any spaces in its name, if you do put a type next to it the compiler can easily pick it up. What does this look like? Like this, for example:

    \.function my_add
        | ~\.I x
        | ~\.I y
        | \.+ \x \y \\
    \\

This looks like a hastle doesn't it? Well, there are a few useful tricks you can use to simplify things. For example, multiple strings in a command argument slot will be interpretted each as a new argument name. The seperators enclose type requirements. So, the above could be rewritten like so:

    \.function my_add
        | ~\.I x y
        | \.+ \x \y
    \\

Of course, this example is supremely useless because as it shows, the built-in function `\.+` already does the same thing (actually, not quite, sine it can take any number of arguments of types natural, integer, or float and sums them, the heirarchy of resulting values being the same as the order I listed them). Perhaps we can make a greeter like all the other language examples do:

    \function greet
        | ~\.S name
        | Hello there, \name . How are you?
    \\

Note that I had to seperate the `.` from the end of `\name`. This is an annoying precaution that you'll have to be mindful of at the moment. I'll fix that at some point in the future, I promise.

## Referencing Functions

Sometimes you want to reference a command itself rather than invoke it. For example, if you want to `\.let` x be an integer. The command for representing an integer value is `\.I`, but if you did `\.let x | \.I \\` the compiler will be confused because it thinks you are invoking `\.I` in the second argument of `\.let`, but there are no subsequent arguments passed to `\.I`, so you'll get an error pointing that out. What you really want to do is _reference_ `\.I` rather than invoke it. Commonly this is termed as using a __pointer__ that referenced where `\.I` is stored.

Fortunately Notery doesn't complicate it to the level of pointers, but uses this notation to create a reference: `~\.I`. You can only create references to command words. For the running example with `\.let`ing x be an integer, the solution is:

    \.let x | ~\.I \\

Another common use of references you'll come across is repetitions or loops. The built-in command for repeating a command a given number of times is `\.loop`. Which is defined something like this (given some internal structure that can't be described in Notery's semantics):

    \function loop
        | ~\.N times
        | ~\.~ command
        | \command \command ... \command
          \* repeats '\times' times \\
    \\

It takes a natural and a command word reference (to just repeat a string, use `\.repeat`). Then is invokes the command word that many times, as observable above. Using this functions looks like this:

    \set message | This is an annoying message! \\
    \loop \.N 10000 | ~\message \\

Of coures, we could have just done this instead,

    \repeat \.N 10000 | \message \\

so this isn't the most interesting example. Here's a better one:

    \function my_log
        | message
        | \.log [!]: \message
    \\

    \function test_log
        | \my_log Hello, is anyone there?
    \\

    \loop \.N 2 | ~\.test_log \\

You may think that currying would be a useful tactic here, and you would be correct, but unfortunately that hasn't been planned for implementation yet.

Note: in `\my_log`'s definition, `message` doesn't have a type annotation, so it is assumed to be a string (`\.S`).