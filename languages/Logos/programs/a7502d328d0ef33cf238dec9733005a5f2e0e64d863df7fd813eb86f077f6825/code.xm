%hook SpringBoard

- (void)applicationDidFinishLaunching:(UIApplication *)application {
    %orig;

    UIAlertController *alert = [UIAlertController
        alertControllerWithTitle:@"Hello, Logos!"
        message:@"A Logos tweak is running."
        preferredStyle:UIAlertControllerStyleAlert];

    UIAlertAction *ok = [UIAlertAction
        actionWithTitle:@"OK"
        style:UIAlertActionStyleDefault
        handler:nil];

    [alert addAction:ok];

    UIWindow *window = [UIApplication sharedApplication].keyWindow;
    [window.rootViewController presentViewController:alert
                                            animated:YES
                                          completion:nil];
}

%end
