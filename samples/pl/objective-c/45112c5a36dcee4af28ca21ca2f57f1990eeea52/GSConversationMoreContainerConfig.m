//
//  GSConversationMoreContainerConfig.m
//  ShangXueLa
//
//  Created by yangqian on 15/10/22.
//  Copyright © 2015年 ShangXueLa. All rights reserved.
//

#import "GSConversationMoreContainerConfig.h"
#import "GSMediaItem.h"

@implementation GSConversationMoreContainerConfig
- (NSArray *)mediaItems
{
    return @[[GSMediaItem item:GSMediaButtonPicture
                   normalImage:[UIImage imageNamed:@"im_add_picture"]
                 selectedImage:[UIImage imageNamed:@"im_add_picture"]
                         title:@"相册"],
             
             [GSMediaItem item:GSMediaButtonShoot
                   normalImage:[UIImage imageNamed:@"im_add_camera"]
                 selectedImage:[UIImage imageNamed:@"im_add_camera"]
                         title:@"拍摄"],
             
             [GSMediaItem item:GSMediaButtonCard
                   normalImage:[UIImage imageNamed:@"im_add_card"]
                 selectedImage:[UIImage imageNamed:@"im_add_card"]
                         title:@"名片"],
             
             [GSMediaItem item:GSMediaButtonCall
                   normalImage:[UIImage imageNamed:@"im_add_phone"]
                 selectedImage:[UIImage imageNamed:@"im_add_phone"]
                         title:@"免费电话"]];
}

- (BOOL)shouldHideItem:(GSMediaItem *)item
{
    BOOL hidden = NO;
    if ([_conversation gsConversationType] == GSConversationChatGroup || [_conversation gsConversationType] == GSConversationClass || [_conversation gsConversationType] == GSConversationUnknown) {
        hidden = item.tag == GSMediaButtonCall;
    }
    if ([_conversation isPublicService]) {
        if (item.tag == GSMediaButtonCall || item.tag == GSMediaButtonCard) {
            hidden = YES;
        }
    }
    return hidden;
}

- (id<GSCellLayoutConfig>)layoutConfigWithMessage:(RCMessage *)message{
    return nil;
}

- (id<GSCellLayoutConfig>)layoutConfigWithCustomMessage:(GSCustomMessage *)customMessage{
    return nil;
}

- (BOOL)disableInputView{
    if (_conversation.gsConversationType == GSConversationClass) {
        if ([GSContacts retrievalClassesWithClassIds:@[_conversation.targetId] autoFill:NO].count==0) {//检查班级是否已经解散
            [SVProgressHUD showErrorWithStatus:@"班级已解散"];
            return YES;
        }else if (![GSContacts retrievalClassUser:CurrentUser.userId InClass:_conversation.targetId]){//检查我是都还在班级中
            [SVProgressHUD showErrorWithStatus:@"你已不在班级中"];
            return YES;
        }
        //    }else if (_conversation.gsConversationType == GSConversationChatGroup){
        //        if (![GSContacts retrievalChatGroupUser:CurrentUser.userId InChatGroup:_conversation.targetId]) {//判断是否还在群聊中
        //            [SVProgressHUD showErrorWithStatus:@"你已不在群聊中"];
        //            return YES;
        //        }
    }else if (_conversation.gsConversationType == GSConversationUnknown){
        [SVProgressHUD showErrorWithStatus:@"你们还不是好友"];
        return YES;
    }
    return NO;
}

@end
