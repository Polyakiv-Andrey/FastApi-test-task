# Issue RSA private key + public key pair

```
## Generate an RSA private key, of size 2048
openssl genrsa -out certs/jwt-private.pem 2048
```
```
## Extract the public key from the key pair, which can be used in a certificate
openssl rsa -in certs/jwt-private.pem -outform PEM -pubout -out certs/jwt-public.pem
```