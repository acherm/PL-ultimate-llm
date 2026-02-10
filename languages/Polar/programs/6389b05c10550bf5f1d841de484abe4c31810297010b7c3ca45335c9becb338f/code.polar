# Define actor types
actor User {}
actor Admin {}

# Define resource types
resource Repository {
  roles = ["owner", "contributor", "reader"];
  permissions = ["read", "write", "delete"];

  "read" if "reader";
  "write" if "contributor";
  "delete" if "owner";

  "contributor" if "owner";
  "reader" if "contributor";
}

# Authorization rules
allow(actor: User, "read", repository: Repository) if
  has_role(actor, "reader", repository);

allow(actor: User, "write", repository: Repository) if
  has_role(actor, "contributor", repository);

allow(actor: Admin, _action, _resource);

# Helper rules
has_role(user: User, role: String, repository: Repository) if
  role in user.roles and
  repository in user.repositories;
