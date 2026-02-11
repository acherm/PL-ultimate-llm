def _my_rule_impl(ctx):
  out = ctx.actions.declare_file(ctx.label.name)
  ctx.actions.write(
      out,
      "Hello from rule %s" % ctx.label,
  )
  return DefaultInfo(files = depset([out]))

my_rule = rule(
    implementation = _my_rule_impl,
)