from models import S2ECodeParser

if __name__ == "__main__":
    #S2ECodeParser.parsePlugin("/home/davide/S2E/s2e/qemu/s2e/Plugins/Debugger.cpp")
    S2ECodeParser.parsePluginsInDir("/home/davide/S2E/s2e/qemu/s2e/Plugins/", [
        "ExecutionTracer.cpp",
        "InstructionCounter.cpp",
        "ModuleTracer.cpp",
        "TestCaseGenerator.cpp",
        "TranslationBlockTracer.cpp",
        "Example.cpp",
        "ModuleExecutionDetector.cpp"])

