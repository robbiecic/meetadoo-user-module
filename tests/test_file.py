cookie = 'jwt=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJlbWFpbCI6InRlc3Q1QHRlc3QuY29tIiwiZXhwIjoxNTgyNzE5NzAzfQ.Wrvy_EQbRNu0x8662FheBlTqRXqf_HnDVcvVykq55JI'
# Locate cookie details if there, if not ignore
jwt_token = "Something Invalid"
try:
    # 'cookie' is case sensistive. Is lower case from browser, upper care from Postman
    try:
        cookie = 'jwt=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJlbWFpbCI6InRlc3Q1QHRlc3QuY29tIiwiZXhwIjoxNTgyNzE5NzAzfQ.Wrvy_EQbRNu0x8662FheBlTqRXqf_HnDVcvVykq55JI'
    except:
        cookie = 'jwt=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJlbWFpbCI6InRlc3Q1QHRlc3QuY29tIiwiZXhwIjoxNTgyNzE5NzAzfQ.Wrvy_EQbRNu0x8662FheBlTqRXqf_HnDVcvVykq55JI'
    print('Cookie - ' + str(cookie))
    # Had to add this as running through AWS, different cookies are added. We want the one starting with jwt
    split_cookie = str(cookie).split(';')
    for x in split_cookie:
        try:
            index = str(x).index("jwt")
            jwt_token = x.replace("jwt", "").replace(
                " ", "").replace("=", "")
        except:
            # Ignore, index will throw an error meaning the "jwt" doesn't exist
            pass
except:
    jwt_token = "Something Invalid"

print('jwt_token - ' + str(jwt_token))
