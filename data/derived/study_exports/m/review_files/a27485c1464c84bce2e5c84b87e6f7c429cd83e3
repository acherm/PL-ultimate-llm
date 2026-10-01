//
//  CWStartScreenViewController.m
//  Sender
//
//  Created by Khalid on 11/8/13.
//  Copyright (c) 2013 pho. All rights reserved.
//

#import "CWStartScreenViewController.h"
#import "CWVideoManager.h"


@interface CWStartScreenViewController ()<CWVideoPlayerDelegate>
@end

@implementation CWStartScreenViewController

- (id)initWithNibName:(NSString *)nibNameOrNil bundle:(NSBundle *)nibBundleOrNil
{
    self = [super initWithNibName:nibNameOrNil bundle:nibBundleOrNil];
    if (self) {
        // Custom initialization
    }
    return self;
}

- (void)viewDidLoad
{
    [super viewDidLoad];
	// Do any additional setup after loading the view.
    [self.navigationController setNavigationBarHidden:YES];
     NSURL * videoURL = [[NSBundle bundleForClass:[self class]] URLForResource:@"video" withExtension:@"mp4"];
    [[[CWVideoManager sharedManager] player] setDelegate:self];
    [[[CWVideoManager sharedManager] player] setVideoURL:videoURL];
    
}

- (void)didReceiveMemoryWarning
{
    [super didReceiveMemoryWarning];
    // Dispose of any resources that can be recreated.
}


- (void)videoPlayerDidLoadVideo:(CWVideoPlayer *)videoPlayer
{
    [self.view addSubview:videoPlayer.playbackView];
    [videoPlayer.playbackView setFrame:CGRectInset(self.view.bounds, 50, 50)];
    [videoPlayer play];
}

- (void)videoPlayerFailedToLoadVideo:(CWVideoPlayer *)videoPlayer withError:(NSError *)error
{
    
}

- (void)videoPlayerPlayToEnd:(CWVideoPlayer *)videoPlayer
{
    
}



@end
