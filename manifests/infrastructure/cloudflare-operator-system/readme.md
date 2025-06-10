# manifests/infrastructure/cloudflare-operator-system/readme.md

Need to create a cert

openssl req -x509 -nodes -days 365 \
 -newkey rsa:2048 \
 -keyout tls.key \
 -out tls.crt \
 -subj "/CN=cloudflare-operator-webhook.cloudflare-operator-system.svc"

flux create secret tls webhook-server-cert \
 --namespace=cloudflare-operator-system \
 --tls-key-file=./tls.key \
 --tls-crt-file=./tls.crt \
 --export > ./manifests/infrastructure/cloudflare-operator-system/webhook-secret.yaml
