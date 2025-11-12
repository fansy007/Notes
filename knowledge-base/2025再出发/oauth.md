#java
# security basic
identity -- store at db, ldap
![[Pasted image 20250428104024.png]]
authenticate is done by LDAP
authorize still managed by application itself

cloud app can't access to LDAP, which will be block for nowadays

## SAML
![[Pasted image 20250428104827.png]]
server1 ask user agent redirect to server2

![[Pasted image 20250428105145.png]]
appication will redirect user to SAML provider, SAML respond will pass back to service application

SAML depends on the browser redirect machanism

SAML have some problems:
>[!note]+ how to secure api calls? (@ web browser side)

>[!note]+ cron jobs call api, there's no user involved


>[!note]+ third party app problem
![[Pasted image 20250428111415.png]]
udemy want access to linkin api, how to calling in secure way?

## oauth 2.0
![[Pasted image 20250428113503.png]]

resource owner: you
resource server: google facebook
client: shutterly app
authorization server: google/facebook oauth server

### client registration
client(shutter fly) will send oauth server its clientid,secret to fetch token

### opague token
![[Pasted image 20250428140920.png]]


### structure token: JWT
resource server can verify the JWT without sending to auth server
using public signing key
![[Pasted image 20250428143211.png]]

## Grant types
ajax client: public client
server side client: confidential client

auth code call -- user id, passrod input the on resource server directly and return auth code for fetch token using
auth code call + PKCE (public client need use PKCE for secure)

Client credentials -- no resource owner, just client define it
REsouce Owner password credentails -- resource owner enter username passwrod, client provide client id, secret to get token directly, this only used resource owner, client is in the sae organization

![[Pasted image 20250428150435.png]]