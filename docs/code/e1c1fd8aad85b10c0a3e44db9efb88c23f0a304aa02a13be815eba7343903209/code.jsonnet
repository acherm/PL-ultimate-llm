// Copyright 2015 Google Inc. All rights reserved.
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//     http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.

local kube = import 'kube.libsonnet';

{
  'service.json': kube.Service('nginx') {
    target_pod: $.deployment.spec.template,
  },

  'deployment.json': kube.Deployment('nginx') {
    spec+: {
      replicas: 3,
      template+: {
        spec+: {
          containers_+: {
            nginx: kube.Container('nginx') {
              image: 'nginx:1.7.9',
              ports_+: {
                http: { containerPort: 80 },
              },
            },
          },
        },
      },
    },
  },

  'configmap.json': kube.ConfigMap('nginx-config') {
    data: {
      'nginx.conf': ||
        user nginx;
        worker_processes auto;
        error_log /var/log/nginx/error.log;
        pid /run/nginx.pid;

        events {
            worker_connections 1024;
        }

        http {
            log_format  main  '$remote_addr - $remote_user [$time_local] "$request" '
                              '$status $body_bytes_sent "$http_referer" '
                              '"$http_user_agent" "$http_x_forwarded_for"';

            access_log  /var/log/nginx/access.log  main;

            sendfile            on;
            tcp_nopush          on;
            tcp_nodelay         on;
            keepalive_timeout   65;
            types_hash_max_size 2048;

            include             /etc/nginx/mime.types;
            default_type        application/octet-stream;

            server {
                listen       80 default_server;
                listen       [::]:80 default_server;
                server_name  _;
                root         /usr/share/nginx/html;

                location / {
                }

                error_page 404 /404.html;
                    location = /40x.html {
                }

                error_page 500 502 503 504 /50x.html;
                    location = /50x.html {
                }
            }
        }
      ||,
    },
  },
}