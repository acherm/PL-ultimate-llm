package httpsonly

violation[{"msg": msg}] {
	ingress := input.review.object
	rule := ingress.spec.rules[_]
	not rule.http
	paths := rule.http.paths
	path := paths[_]
	# Fails if `path` is not defined
	# Fails if `path.backend` is not defined
	# Fails if `path.backend.service` is not defined
	# Fails if `path.backend.service.port` is not defined
	# Fails if `path.backend.service.port.name` is not defined
	# Fails if `path.backend.service.port.number` is not defined
	port := path.backend.service.port
	port.name == "http"
	port.number == 80
	msg := sprintf("Ingress rule for host %v and path %v is not HTTPS. Port name is %v and number is %v", [rule.host, path.path, port.name, port.number])
}

violation[{"msg": msg}] {
	ingress := input.review.object
	not ingress.spec.tls
	msg := sprintf("Ingress %v does not have TLS configured", [ingress.metadata.name])
}