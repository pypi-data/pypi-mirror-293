# zuto
a lite-r version of [zutomator](https://github.com/ZackaryW/zutomator)

## Install
```bash
pip install zuto
```

## Example

```py
class ExampleTest:
    # will print the string below
    """
    daily automated tests
    """

    @step
    def test_scenario_delta(ctx: Ctx):
        """
        uses custom test runner
        
        """
        open_detached("notepad.exe")
        ctx.wait() 
        
    test_scenario_delta.timeout = 10 # set timeout
```

## Upcoming Changes
* in a future version, `ctx.wait()` will monitor current processes and windows
* project zutomator will merge with this project after this lite version is stable
