s2e = {
	 kleeArgs = {}
}

plugins = {
	"EdgeKiller",
	"ModuleExecutionDetector",
	 "HostFiles" ,
	 "BaseInstructions" 
}

pluginsConfig = {}

pluginsConfig.EdgeKiller = {
	aaa={
		qqq={
			addresses= {3, 4, 7, 13}
		}
	}
}

pluginsConfig.ModuleExecutionDetector = {
	trackAllModules=true,
	configureAllModules=true,
	aaa={
		moduleName=aaa,
		kernelMode=false
	}
}

pluginsConfig.HostFiles = {
	 baseDirs = {"/home/davide/S2E/python/s2e2-gui/temp-dir/"}
}
