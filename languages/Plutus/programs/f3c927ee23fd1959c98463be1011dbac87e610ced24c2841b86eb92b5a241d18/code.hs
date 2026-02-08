{-# LANGUAGE DataKinds #-}
{-# LANGUAGE TemplateHaskell #-}
{-# LANGUAGE NoImplicitPrelude #-}

module AlwaysSucceeds where

import PlutusTx
import PlutusTx.Prelude
import Plutus.V2.Ledger.Api

-- A validator that always succeeds
alwaysSucceedsValidator :: BuiltinData -> BuiltinData -> BuiltinData -> ()
alwaysSucceedsValidator _ _ _ = ()

validator :: Validator
validator = mkValidatorScript $$(PlutusTx.compile [|| alwaysSucceedsValidator ||])
