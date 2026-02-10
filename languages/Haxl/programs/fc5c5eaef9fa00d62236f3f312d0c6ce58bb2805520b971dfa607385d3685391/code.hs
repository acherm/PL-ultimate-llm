-- Simple Haxl example demonstrating concurrent data fetching
{-# LANGUAGE DeriveDataTypeable #-}
{-# LANGUAGE GADTs #-}
{-# LANGUAGE StandaloneDeriving #-}
{-# LANGUAGE TypeFamilies #-}
{-# LANGUAGE MultiParamTypeClasses #-}

module Example where

import Haxl.Core
import Data.Typeable

-- Define a data source for user lookups
data UserRequest a where
  GetUserName :: Int -> UserRequest String
  deriving Typeable

deriving instance Eq (UserRequest a)
deriving instance Show (UserRequest a)

instance Show1 UserRequest where show1 = show

instance StateKey UserRequest where
  data State UserRequest = UserState {}

instance DataSourceName UserRequest where
  dataSourceName _ = "UserDataSource"

instance DataSource u UserRequest where
  fetch _state _flags _userEnv = SyncFetch $ \blockedFetches -> do
    mapM_ fetch1 blockedFetches
    where
      fetch1 (BlockedFetch (GetUserName uid) v) = do
        putSuccess v ("user_" ++ show uid)

-- Example computation
getUserInfo :: Int -> GenHaxl u String
getUserInfo userId = do
  name <- dataFetch (GetUserName userId)
  return $ "User: " ++ name
