---

# How to Make a Plugin

## Clone McLium

```bash
git clone https://github.com/your-username/McLium.git
cd McLium
```

## Create Your Plugin Directory

### Navigate to the plugins folder

```bash
cd plugins
```

### Create your plugin folder

In this example, we create a plugin named `example`.

```bash
mkdir example
cd example
```

Your structure should now look like:

```
McLium/
 ├── plugins/
 │    └── example/
```

---

## Configure plugin.yml

Inside your plugin folder, create a file named:

```
plugin.yml
```

This file defines your plugin metadata and tells McLium how to load it.

### Example plugin.yml

```yaml
main: 'entry_point.Main'
name: "example"
description: "this is example plugin"
version: 1.0.0
author: ["kenftr"]

require_libraries: []

depend: []
softdepend: []

metadata:
  type: "utils"
  category: "utils"
```

### Field Explanation

| Field             | Description                                          |
| ----------------- | ---------------------------------------------------- |
| main              | Entry point class in the format `filename.ClassName` |
| name              | Plugin name (must match folder name)                 |
| description       | Short description of the plugin                      |
| version           | Plugin version                                       |
| author            | List of authors                                      |
| require_libraries | External libraries required                          |
| depend            | Required plugins that must load first                |
| softdepend        | Optional plugin dependencies                         |
| metadata.type     | Plugin classification                                |
| metadata.category | Plugin category                                      |

Important notes:

* `main` must follow the format `filename.ClassName`
* Do not include `.py`
* File and class names are case-sensitive
* YAML must use spaces, not tabs

After this step:

```
McLium/
 ├── plugins/
 │    └── example/
 │         └── plugin.yml
```

---

## Create the Entry Point

In `plugin.yml`, we defined:

```yaml
main: 'entry_point.Main'
```

This means:

* The file must be `entry_point.py`
* The class inside must be `Main`

Create the file:

```bash
touch entry_point.py
```

Now your structure should look like:

```
McLium/
 ├── plugins/
 │    └── example/
 │         ├── plugin.yml
 │         └── entry_point.py
```

---

## Create a Subcommand

McLium supports two types of modules:

* TaskModule: runs automatically when McLium starts
* SubCommandModule: runs only when invoked from the CLI

Here we create a subcommand.

### Example implementation

```python
from mclium.mclium_types import Flag
from mclium.api import SubCommandModule


class Main(SubCommandModule):

    def __init__(self):
        flags = [
            Flag(
                short="-e",
                long="--example",
                dest="example",
                type=str,
                required=True,
                help="Example command"
            )
        ]

        super().__init__("example", flags)

    def on_command(self, args):
        """
        Called when the subcommand is executed.

        args contains all parsed CLI arguments.
        Each Flag's `dest` becomes an attribute of this object.

        Example:
            python Mclium.py example -e "Hello"

        Then:
            args.example == "Hello"
        """

        print(f"Message: {args.example}")
```

---

## Understanding Flag

Each `Flag` defines a CLI argument for your subcommand.

### Example

```python
Flag(
    short="-e",
    long="--example",
    dest="example",
    type=str,
    required=True,
    help="Example command"
)
```

### Flag parameters

| Parameter | Type | Description                                       |
| --------- | ---- | ------------------------------------------------- |
| short     | str  | Short version of the flag, for example `-e`       |
| long      | str  | Long version of the flag, for example `--example` |
| dest      | str  | Attribute name used inside `args`                 |
| type      | type | Data type such as `str`, `int`, `float`, `bool`   |
| required  | bool | Whether the argument is mandatory                 |
| help      | str  | Help message shown in CLI usage                   |

### How dest works

If you define:

```python
dest="example"
```

You must access it like this inside `on_command`:

```python
print(args.example)
```

---

## Supported type values

| Type  | Example Input | Parsed Result |
| ----- | ------------- | ------------- |
| str   | hello         | "hello"       |
| int   | 123           | 123           |
| float | 3.14          | 3.14          |
| bool  | true          | True          |

---

## Running the Subcommand

```bash
python Mclium.py example -e "Hello World"
```

Output:

```
Message: Hello World
```

---

## Multiple Flags Example

```python
flags = [
    Flag("-e", "--example", "example", str, True, "Example"),
    Flag("-n", "--number", "number", int, False, "Optional number")
]
```

You can access:

```python
args.example
args.number
```

If the optional flag is not provided:

```
args.number == None
```

---

## Create a Task

```python
from mclium.api
```
