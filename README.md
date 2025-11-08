# AlgoXCC

A Rust implementation of Donald Knuth’s algorithm for solving an exact cover with colors problem using the Dancing Cells data structure.

## Exact cover problems

The exact cover problem involves a set of items and a set of options, where each option is a subset of items. A solution to the problem is any subset of options in which all items are represented exactly once.

The generalized exact cover extends this with two types of items:
- primary items, which, as before, must be covered exactly once, and
- secondary items, which must be covered at most once.

The exact cover with colors problem extends this by assigning colors to secondary items within options, allowing a secondary item to be covered by multiple options if they have the same color.

## Usage

### The logic

The inputs to the algorithm are defined in a Problem with:
- primary items: list of unique item names as strings
- secondary items: list of unique item names as strings
- options: list of Options

Where an Option have:
- label: unique label as string identifying an option
- primary items: list of primary items covered by option as strings
- secondary items: list of secondary items covered by option

Secondary items covered by an option are tuples with two elements as strings:
- first element: the secondary item covered by the option
- second element: color used to cover the secondary item

Where a blank color for a secondary item is regarded as a unique color.

With prerequisites:
- A Problem must have at least one primary item.
- All items must be unique (also across primary and secondary items).
- All primary items must be represented in at least one Option.
- All items in an Option must exist in Problem list of items

### The code

