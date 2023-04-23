# MockServer

You'll need to issue a self-signed certificate to start the server

First install OpenSSL

Then generate a self-signed certificate using OpenSSL
1. Open command line and navigate to the MockServer directory
2. Generate a private key:
openssl genrsa -out server.key 2048
3. Generate a certificate signing request (CSR):
openssl req -new -key server.key -out server.csr
4. Generate a self-signed certificate using the CSR:
openssl x509 -req -days 365 -in server.csr -signkey server.key -out server.crt

