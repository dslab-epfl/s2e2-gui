s2e = {
	 kleeArgs = {}
}

plugins = {
	"Example",
	 "HostFiles" 
}

pluginsConfig = {}

pluginsConfig.Example = {
	traceBlockTranslation = false,
	traceBlockExecution = true
}

pluginsConfig.HostFiles = {
	 baseDirs = {"/home/davide/S2E/python/s2e2-gui/temp-dir/"}
}
