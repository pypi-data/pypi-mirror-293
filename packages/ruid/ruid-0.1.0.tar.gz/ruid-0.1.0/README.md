# Description

Generates reasonably unique (slim chance of duplicates) and readable (avoids characters that look similar) fixed width string identifiers. These identifiers are useful as API tokens, database record identifiers (primary keys, etc) among other things.

## Installation

```shell
pip install ruid
```

or

```shell
poetry add ruid
```

## Length considerations

The function uses current date and time to determine part of the random string. This has the advantage of ensuring fewer collisions at different timestamps but also means that a length of 6 would result in same token generated within the same second. A reasonable default length of 10 ensures more than 6 million tokens per second. Length below 6 is not supported.
