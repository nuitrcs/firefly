function Component()
{
}

Component.prototype.createOperations = function(archive)
{
    component.createOperations(archive);

	if(typeof systemInfo != "undefined" && systemInfo.kernelType != "winnt") {
	    // NOTE: This is specific for OSX, not linux!
	    	
	    // Create links to Chromium embedded framework resources file
		component.addOperation("Execute", "mkdir", "-p", "@TargetDir@/Contents/Frameworks/Chromium Embedded Framework.framework", 
			"UNDOEXECUTE", "rm", "-rf", "@TargetDir@/Contents/Frameworks/Chromium Embedded Framework.framework");
	    
	    // Create links to Chromium embedded framework resources file
		component.addOperation("Execute", "ln", "-s", "@TargetDir@/bin/Resources", "@TargetDir@/Contents/Frameworks/Chromium Embedded Framework.framework/Resources");
		component.addOperation("Execute", "ln", "-s", "@TargetDir@/bin", "@TargetDir@/Contents/MacOS");

		// Create links to executable and data in /usr
		component.addOperation("Execute", "ln", "-s", "@TargetDir@/Contents/MacOS/orun", "/usr/local/bin/firefly", 
			"UNDOEXECUTE", "rm", "/usr/local/bin/firefly");

		component.addOperation("Execute", "ln", "-s", "@TargetDir@/UninstallFirefly.app/Contents/MacOS/UninstallFirefly", "/usr/local/bin/firefly-uninstall", 
			"UNDOEXECUTE", "rm", "/usr/local/bin/firefly-uninstall");
    }
}