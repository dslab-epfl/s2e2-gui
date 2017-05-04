s2e = {
	 kleeArgs = {}
}

plugins = {
	"InstructionCounter",
	"ExecutionTracer",
	"ModuleExecutionDetector",
	 "HostFiles" ,
	 "Vmi" ,
	 "BaseInstructions" 
}

pluginsConfig = {}

pluginsConfig.ModuleExecutionDetector = {
	trackAllModules=true,
	trackExecution=true,
	configureAllModules=true
}

pluginsConfig.HostFiles = {
	 baseDirs = {"/home/davide/tmp/s2e/projects/binary"},
	 allowWrite = true,
}
pluginsConfig.Vmi = {
	 baseDirs = {"/home/davide/tmp/s2e/projects/binary"}
}
dofile('library.lua')
add_plugin("LinuxMonitor")
pluginsConfig.LinuxMonitor = {
-- Kill the execution state when it encounters a segfault
    terminateOnSegFault = true,
-- Kill the execution state when it encounters a trap
terminateOnTrap = true,
}
-------------------------------------------------------------------------------
-- This generates test cases when a state crashes or terminates.
-- If symbolic inputs consist of symbolic files, the test case generator writes
-- concrete files in the S2E output folder. These files can be used to
-- demonstrate the crash in a program, added to a test suite, etc.
add_plugin("TestCaseGenerator")
pluginsConfig.TestCaseGenerator = {
    generateOnStateKill = true,
    generateOnSegfault = true
}
