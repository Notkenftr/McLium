# How to make a plugin

## First. You need to clone McClium to your computer.

```bash
git clone https://github.com/your-username/McLium.git
cd McLium
```

## Second. Create Your Plugin Directory
### **Step 1 - Navigate to the plugins folder**
Go to your project root and open the plugins directory.
```bash
cd plugins
```
### **Step 2 - Create your plugin folder**
Create a new folder for your plugin.<br>
In this example, we will create a plugin named **example**.
```bash
mkdir example
cd example
```
Your structure should now look like this:
```
McLium/
 ├── plugins/
 │    └── example/
```
## Third. Configure plugin.yml
Inside your plugin folder, create a file named:
``plugin.yml``
This file defines your plugin metadata and tells McLium how to load it.

### 📄 Example plugin.yml

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
### 🔍 Field Explanation
| Field               | Description                                        |
| ------------------- | -------------------------------------------------- |
| `main`              | Entry point class (Python path to your main class) |
| `name`              | Plugin name (must match folder name)               |
| `description`       | Short description of your plugin                   |
| `version`           | Plugin version                                     |
| `author`            | List of plugin authors                             |
| `require_libraries` | External libraries required by the plugin          |
| `depend`            | Required plugins that must load before this one    |
| `softdepend`        | Optional plugins that enhance functionality        |
| `metadata.type`     | Plugin type classification                         |
| `metadata.category` | Plugin category for organization                   |

**After creating plugin.yml, your folder should look like this:**

```
McLium/
 ├── plugins/
 │    └── example/
 │         └── plugin.yml
```

### 💡 Important
- main must point to a valid Python class.<br>
- YAML indentation must use spaces (not tabs).

# Fourth. Create entry points and subcommands.
**Note: McLium supports two types of commands: tasks and subcommands. Tasks run automatically when McLium starts, while subcommands only run when you call them.**

### **Step 1 - Create the Entry File**
In your **plugin.yml**, you defined:
```yaml
main: 'entry_point.Main'
```
This means:

- entry_point → The Python file name (entry_point.py)

- Main → The class inside that file

So you must create a file named:
```bash
touch entry_point.py
```
**Your structure should now look like:**
```
McLium/
 ├── plugins/
 │    └── example/
 │         ├── plugin.yml
 │         └── entry_point.py
```

### How main Works?
**Format:**
```
filename.ClassName
```
**Example:**

| `main` value       | Required file    | Required class |
| ------------------ | ---------------- | -------------- |
| `entry_point.Main` | `entry_point.py` | `class Main`   |
| `core.Start`       | `core.py`        | `class Start`  |

**If the file or class does not match exactly, McLium will fail to load the plugin.**

### 💡 Important

- File name must match exactly.

- Class name is case-sensitive.

- Do not include .py in the main path.

### Step 2 - create subcommand

Open the entry point file you created earlier (based on main in plugin.yml).

In this example, we are creating a Subcommand, which only runs when explicitly invoked from the CLI.

### Example Implementation

```python
from mclium.mclium_types import Flag
from mclium.api import SubCommandModule


class Main(SubCommandModule):

    def __init__(self):
        flags = [
            Flag(short="-e",
                 long="--example",
                 dest="example",
                 type=str,
                 required=True,
                 help="Example command",
                 )
        ]

        super().__init__("example", flags)
        #                   ^         ^
        #                   name     flags
    def on_command(self, args):
        print(f"Message: {args.example}")
```
### Parameters in Flag
The Flag class defines a CLI argument for your subcommand.
Each parameter controls how the argument behaves.
**Example**
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
### **🔍 Parameter Explanation**

| Parameter  | Type   | Description                                               |
| ---------- | ------ | --------------------------------------------------------- |
| `short`    | `str`  | Short flag version (e.g., `-e`)                           |
| `long`     | `str`  | Long flag version (e.g., `--example`)                     |
| `dest`     | `str`  | Variable name used inside `args`                          |
| `type`     | `type` | Data type of the argument (`str`, `int`, `float`, `bool`) |
| `required` | `bool` | Whether this argument is mandatory                        |
| `help`     | `str`  | Help message shown in CLI usage                           |

### **How dest Works**
If you define:
```python
dest="example"
```
You must access it like this inside on_command():
```python 
def execute(self, args):
    print(args.example)
```

### Supported type Values

| Type    | Example Input | Parsed Result |
| ------- | ------------- | ------------- |
| `str`   | `"hello"`     | `"hello"`     |
| `int`   | `123`         | `123`         |
| `float` | `3.14`        | `3.14`        |
| `bool`  | `true`        | `True`        |


### 🔍 Explanation

|      Component       | Description                          |
|:--------------------:| ------------------------------------ |
|  `SubCommandModule`  | Base class for CLI-based plugins     |
|        `Flag`        | Defines command-line arguments       |
| `super().__init__()` | Registers the command name and flags |
|     `on_command()`      | Runs when the command is called      |

### Running the Subcommand
You can execute your plugin using:
```bash 
python Mclium.py example -e "Hello World"
```
Output:
```
Message: Hello World
```
