//
//  CustomAlertView.m
//  CakeLove
//
//  Created by radar on 10-3-29.
//  Copyright 2010 RED/SAFI. All rights reserved.
//

#import "CustomAlertView.h"


@implementation CustomAlertView
@synthesize delegate=_delegate;


-(id)initWithTitle:(NSString*)title contentView:(UIView*)contentView delegate:(id)dele leftBtnImage:(UIImage*)leftBtnImage rightBtnImage:(UIImage*)rightBtnImage
{
	CGRect frame = CGRectMake(0.0, 0.0, 320.0, 480.0);
    if (self = [super initWithFrame:frame]) {
        // Initialization code
		self.delegate = dele;
		
		self.backgroundColor = [UIColor clearColor];
		
		UIView *backView = [[UIView alloc] initWithFrame:frame];
		backView.backgroundColor = [UIColor blackColor];
		backView.alpha = 0.5;
		backView.tag = layerBackView;
		[self addSubview:backView];
		
		
		//add others
		CGRect contentFrame = CGRectZero;
		if(contentView != nil) contentFrame = contentView.frame;
		
		//init alertView
		float alertHeight = 50+70+contentFrame.size.height;
		_alertView = [[UIView alloc] initWithFrame:CGRectMake(20.0, (480.0-alertHeight)/2, 280.0, alertHeight)];
		_alertView.center = self.center;
		_alertView.tag = layerAlertView;
		
		
		//backgroundImage
		UIImageView *bgTopImageView = [[UIImageView alloc] initWithFrame:CGRectMake(0.0, 0.0, 280.0, 40.0)];
		bgTopImageView.image = [UIImage imageNamed:@"custom_alert_bg_top.png"];
		bgTopImageView.tag = layerTopImage;
		[_alertView addSubview:bgTopImageView];
		
		UIImageView *bgMidImageView = [[UIImageView alloc] initWithFrame:CGRectMake(0.0, 40.0, 280.0, alertHeight-40.0-10.0)];
		bgMidImageView.image = [UIImage imageNamed:@"custom_alert_bg_middle.png"];
		bgMidImageView.tag = layerMidImage;
		[_alertView addSubview:bgMidImageView];
		
		UIImageView *bgBtmImageView = [[UIImageView alloc] initWithFrame:CGRectMake(0.0, alertHeight-10.0, 280.0, 10.0)];
		bgBtmImageView.image = [UIImage imageNamed:@"custom_alert_bg_btm.png"];
		bgBtmImageView.tag = layerBtmImage;
		[_alertView addSubview:bgBtmImageView];
		
		
		//shadow
		UIImageView *shadowImageView = [[UIImageView alloc] initWithFrame:CGRectMake(0.0, 0.0, 280.0, 40.0)];
		shadowImageView.image = [UIImage imageNamed:@"GlossaryBack_hi.png"];
		shadowImageView.tag = layerShadow;
		[_alertView addSubview:shadowImageView];
		
		
		//title
		UILabel *titleLabel = [[UILabel alloc] initWithFrame:CGRectMake(10.0, 5.0, 260.0, 40.0)];
		titleLabel.textAlignment = NSTextAlignmentLeft;
		titleLabel.font = [UIFont boldSystemFontOfSize:20.0];
		titleLabel.adjustsFontSizeToFitWidth = YES;
		titleLabel.textColor = [UIColor whiteColor];
		titleLabel.backgroundColor = [UIColor clearColor];
		titleLabel.text = title;
		titleLabel.tag = layerTitle;
		[_alertView addSubview:titleLabel];
		
		
		//contentView
		if(contentView != nil)
		{
			CGRect newContentFrame = contentFrame;
			newContentFrame.origin.x = (280-contentFrame.size.width)/2;
			newContentFrame.origin.y = 50.0;
			contentView.frame = newContentFrame;
			contentView.tag = layerContent;
			[_alertView addSubview:contentView];
		}
		
		//leftbtn
		if(leftBtnImage != nil)
		{
			UIButton *leftBtn = [[UIButton alloc] initWithFrame:CGRectMake(10.0, alertHeight-15.0-leftBtnImage.size.height, leftBtnImage.size.width, leftBtnImage.size.height)];
			[leftBtn setImage:leftBtnImage forState:UIControlStateNormal];
			[leftBtn addTarget:self action:@selector(leftBtnAction:) forControlEvents:UIControlEventTouchUpInside];
			leftBtn.tag = layerLeftBtn;
			[_alertView addSubview:leftBtn];
		}
		
		
		//rightbtn
		if(rightBtnImage != nil)
		{
			UIButton *rightBtn = [[UIButton alloc] initWithFrame:CGRectMake(280.0-10.0-rightBtnImage.size.width, alertHeight-15.0-rightBtnImage.size.height, rightBtnImage.size.width, rightBtnImage.size.height)];
			[rightBtn setImage:rightBtnImage forState:UIControlStateNormal];
			[rightBtn addTarget:self action:@selector(rightBtnAction:) forControlEvents:UIControlEventTouchUpInside];
			rightBtn.tag = layerRightBtn;
			[_alertView addSubview:rightBtn];
		}
		
    }
    return self;
}



- (void)drawRect:(CGRect)rect {
    // Drawing code
	
}




#pragma mark -
#pragma mark own use
-(void)leftBtnAction:(id)sender
{
	if(self.delegate &&[(NSObject*)self.delegate respondsToSelector:@selector(customAlertView:clickedButtonAtIndex:)])
	{
		[self.delegate customAlertView:self clickedButtonAtIndex:indexLeft];
	}
	
	[self removeFromSuperview];
}
-(void)rightBtnAction:(id)sender
{
	if(self.delegate &&[(NSObject*)self.delegate respondsToSelector:@selector(customAlertView:clickedButtonAtIndex:)])
	{
		[self.delegate customAlertView:self clickedButtonAtIndex:indexRight];
	}
	
	[self removeFromSuperview];
}

-(void)MoveViewAnimation:(UIView*)mView
{
	_alertView.transform = CGAffineTransformMakeScale(0.1, 0.1);
	
	[UIView beginAnimations:@"movement" context:(__bridge void * _Nullable)(mView)];
	[UIView setAnimationCurve:UIViewAnimationCurveEaseInOut]; 
	[UIView setAnimationDuration:0.2];
	[UIView setAnimationDelegate:self];
	[UIView setAnimationDidStopSelector:@selector(animationDidStop:finished:context:)];
	
	_alertView.transform = CGAffineTransformMakeScale(1.1, 1.1);
	
	[UIView commitAnimations];
}
-(void)MoveViewAnimationZoomOut:(UIView*)mView
{
	[UIView beginAnimations:@"movement zoom out" context:(__bridge void * _Nullable)(mView)];
	[UIView setAnimationCurve:UIViewAnimationCurveEaseInOut]; 
	[UIView setAnimationDuration:0.2];
	[UIView setAnimationDelegate:self];
	[UIView setAnimationDidStopSelector:@selector(animationDidStop:finished:context:)];
	
	_alertView.transform = CGAffineTransformMakeScale(0.9, 0.9);
	
	[UIView commitAnimations];
}
-(void)MoveViewAnimationZoomIn:(UIView*)mView
{
	[UIView beginAnimations:@"movement zoom in" context:nil]; 
	[UIView setAnimationCurve:UIViewAnimationCurveEaseInOut]; 
	[UIView setAnimationDuration:0.2];
	
	_alertView.transform = CGAffineTransformMakeScale(1.0, 1.0);

	
	[UIView commitAnimations];
}

- (void) animationDidStop:(NSString *)animationID finished:(NSNumber *)finished context:(void *)context
{
	if(finished ){
		if([animationID isEqualToString:@"movement"])
			[self MoveViewAnimationZoomOut:(__bridge UIView*)context];
		if([animationID isEqualToString:@"movement zoom out"])
			[self MoveViewAnimationZoomIn:(__bridge UIView*)context];
	}
}




#pragma mark -
#pragma mark out use
-(void)show
{
	[self addSubview:_alertView];
	[self MoveViewAnimation:_alertView];
	
	[[UIApplication sharedApplication].keyWindow addSubview:self];
}





@end
