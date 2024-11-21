# JWT

Json web token



- Client call server 

​	-> server give client JWT token

​	-> next time client call server for real request can input JWT token @ header



Authorization: token

notice JWT token can set expire time,  if token expired, client should ask a new one



- Header.payload.signature



Header payload is base64 encode

```sh
{"alg":"HS256","typ":"JWT"}
{"userId":123,"userName":"Lee","url":"http:www.baidu.com","exp":1691927255}
```

Signare gen by algorithem you provide, and input is header.payload encode by key you provide, then base64 this byte



```gradle
implementation group: 'com.auth0', name: 'java-jwt', version: '4.4.0'
```



```java
    String key = "123123";
    @Test
    /**
     * header.payload.signature
     * eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9
     * .eyJ1c2VySWQiOjEyMywidXNlck5hbWUiOiJMZWUiLCJ1cmwiOiJodHRwOnd3dy5iYWlkdS5jb20iLCJleHAiOjE2OTE5MjQxNTB9
     * .za9NJAxkLD2cGcYpKA8afu_vnll5Dpr2nDqkVsVr2U0
     */    
	public void testJwt() {
        Calendar c =Calendar.getInstance();
        c.add(Calendar.SECOND, 60*5);

        JWTCreator.Builder builder = JWT.create()
                // payload
                .withClaim("userId",123)
                .withClaim("userName", "Lee")
                .withClaim("url", "http:www.baidu.com")
                .withExpiresAt(c.getTime());

        // similar to MDS, need a input string(salt)
        String token = builder.sign(Algorithm.HMAC256(key));
        System.out.println(token);

        // verify
        try {
            DecodedJWT jwtResult = JWT.require(Algorithm.HMAC256(key)).build().verify(token);
            System.out.println(new String(Base64.getDecoder().decode(jwtResult.getHeader())));
            System.out.println(new String(Base64.getDecoder().decode(jwtResult.getPayload())));
            System.out.println(jwtResult.getSignature());
            jwtResult.getClaims().entrySet().forEach(entry -> System.out.println(String.format("%s=%s", entry.getKey(),entry.getValue().asString())));
        } catch (JWTVerificationException e) {
            throw new RuntimeException(e);
        } catch (IllegalArgumentException e) {
            throw new RuntimeException(e);
        }
    }
```

