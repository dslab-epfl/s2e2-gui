from models import S2ECodeParser

if __name__ == "__main__":
    #S2ECodeParser.parsePlugin("/home/davide/S2E/s2e/qemu/s2e/Plugins/Debugger.cpp")
    #S2ECodeParser.parsePluginsInDir("/home/davide/S2E/s2e/qemu/s2e/Plugins/", [
    #    "ExecutionTracer.cpp",
    #    "InstructionCounter.cpp",
    #    "ModuleTracer.cpp",
    #    "TestCaseGenerator.cpp",
    #    "TranslationBlockTracer.cpp",
    #    "Example.cpp",
    #    "StateManager.cpp",
    #    "EdgeKiller.cpp",
    #    "ModuleExecutionDetector.cpp"])

    S2ECodeParser.parsePluginsInDir("/home/davide/tmp/s2e/source/s2e/libs2eplugins/src/s2e/Plugins", [
	"CallSiteMonitor.cpp",
	"ExecutionTracer.cpp",
	"BasicBlockCoverage.cpp",
	"ProcessExecutionDetector.cpp",
	"ModuleExecutionDetector.cpp",
	"TranslationBlockCoverage.cpp",
	"ControlFlowGraph.cpp",
	"InstructionCounter.cpp", 
	"SeedSearcher.cpp",
	"MultiSearcher.cpp",
    "TestCaseGenerator.cpp",
	"SeedScheduler.cpp"])
	

