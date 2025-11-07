(module accounts-admin GOVERNANCE
  "An accounts module to demonstrate reading data from other modules."

  (defcap GOVERNANCE ()
    "Give the admin full access to the module."
    (enforce-guard (keyset-ref-guard 'accounts-admin-keyset)))
)

(module accounts 'accounts-admin-keyset
  "A simple accounts module."

  (defschema account
    "Row type for accounts table."
    balance:decimal
    data:object)

  (deftable accounts:{account})

  (defun create-account (id:string initial-balance:decimal)
    "Create a new account."
    (insert accounts id
      { "balance": initial-balance,
        "data": {} }))

  (defun get-balance (id:string)
    "Get an account's balance."
    (with-read accounts id { "balance" := balance }
      balance))

  (defun pay (from:string to:string amount:decimal)
    "Pay money from one account to another."
    (with-read accounts from { "balance" := from-balance }
      (with-read accounts to { "balance" := to-balance }
        (enforce (> amount 0.0) "Negative Transaction Amount")
        (enforce (>= from-balance amount) "Insufficient Funds")
        (update accounts from
          { "balance": (- from-balance amount) })
        (update accounts to
          { "balance": (+ to-balance amount) })
        (format "{} paid {} to {}" [from, amount, to]))))
)

(create-table accounts)