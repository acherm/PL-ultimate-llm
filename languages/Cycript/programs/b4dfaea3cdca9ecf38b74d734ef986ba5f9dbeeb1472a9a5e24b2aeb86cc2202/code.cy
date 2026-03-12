// List installed applications via SpringBoard using Cycript
var SBApplicationController = objc_getClass("SBApplicationController");
var appController = [SBApplicationController sharedInstance];
var apps = [appController allApplications];
var count = [apps count];

for (var i = 0; i < count; i++) {
    var app = [apps objectAtIndex:i];
    var name = [app displayName];
    var bundleId = [app bundleIdentifier];
    NSLog(@"%@: %@", name, bundleId);
}
