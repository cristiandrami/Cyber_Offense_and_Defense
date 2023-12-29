import jwt
token="eyJraWQiOiI3YTM3YjBlOS1kMWQ5LTQyNzAtYjhlNS0wNzJmN2IxNTZjYTUiLCJhbGciOiJSUzI1NiJ9.eyJpc3MiOiJwb3J0c3dpZ2dlciIsInN1YiI6IndpZW5lciIsImV4cCI6MTcwMjc1NjIyM30.Rl6__KUvhYycVNMyDxsjvSjRyEsUP2EOAXbsbVW0Zql_5ZmMHcgXhYPElDKRJYZqztipgVDE-4aacsKeMO3THTkY8ry06Aw586HkU5ydes0WnZQRpRD-43DDV2B1A0pFZFtF2Q0xB4cRND56VM87hpbNNaEs-DEyr9AlUE5h5Q6C5P_kEiKp9_l4PTERy-wNjcYHXeEGcA3WKTxlQ9gCYuRxdrHFS5izIyLd-0ImRlui0MnKYINxLCVl_SP6YYe_CSS7zKZx_bwNc2eTsAKZiC_G0PBE3zt0whSYYH2VOCEcztDUA0WIL_v-PcYWre_E12d_UdTSxPB9ZcmF2VEMWg"
decoded = jwt.decode(token, options={"verify_signature": False}) # works in PyJWT >= v2.0
print (decoded)


"""TO ENCODE
key='super-secret'
payload={"id":"1","email":"myemail@gmail.com" }
token = jwt.encode(payload, key)
print (token)"""
