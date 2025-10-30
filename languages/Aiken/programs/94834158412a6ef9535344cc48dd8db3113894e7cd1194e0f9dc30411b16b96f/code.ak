use aiken/builtin

validator always_succeeds {
  spend: |ctx: ScriptContext| -> Bool {
    true
  }
}