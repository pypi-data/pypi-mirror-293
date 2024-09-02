import os
from zuto.ext import step
from zuto.runner import Ctx, Runner
from zuu.stdpkg.subprocess import open_detached

class ExampleTest:
    """
    daily automated tests
    """

    @step
    def test_scenario_alpha(ctx: Ctx):
        """
        uses custom macro suite
        """
    
    @step
    def test_scenario_beta(ctx: Ctx):
        """
        uses automated test framework
        """

    @step
    def test_scenario_gamma(ctx: Ctx):
        """
        uses specialized test tool
        """

    @step
    def test_scenario_delta(ctx: Ctx):
        """
        uses custom test runner
        
        """
        open_detached("notepad.exe")
        ctx.wait()
        

    test_scenario_delta.timeout = 10

    @step
    def test_scenario_epsilon(ctx: Ctx):
        pass

os.environ["ZUTO_SKIP_STEPS"] = "test_scenario_alpha"
Runner(ExampleTest)