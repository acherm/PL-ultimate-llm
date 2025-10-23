package main

import (
	"list"
	"strings"
)

// The design for our application
#App: {
	// The application name
	name: string & strings.MaxRunes(12)
	// The labels for the application
	labels: [string]: string
	// The containers for the application
	containers: [ID=#ID]: #Container & {
		// default the container name to the app name and container id
		name: "\(name)-\(ID)"
	}
}

// The container definition
#Container: {
	// The container name
	name: string
	// The container image
	image: string
	// The container command
	command?: [...string]
	// The container environment variables
	env?: [string]: string
}

// our application instance
app: #App & {
	name:   "test"
	labels: owner: "hof"
	containers: {
		// the first container
		web: {
			image: "nginx:latest"
			env: {
				FOO: "bar"
				BAR: "baz"
			}
		}
		// the second container
		db: {
			image: "postgres:12"
			env: {
				POSTGRES_USER:     "postgres"
				POSTGRES_PASSWORD: "password"
			}
		}
	}
}

// Some extra containers to add to the app
more: containers: {
	// the third container
	cache: {
		image: "redis:latest"
	}
}

// Unify the app with the extra containers
// list.Concat will merge the containers from both sources
// The result is a new, final application design
final: app & {
	containers: list.Concat([app.containers, more.containers])
}
