import time
from hashlib import md5, sha256, sha3_512

from passlib.context import CryptContext 
from jose import jwt # pip install python-jose 



if __name__ == "__main__":

    pas = "my_pasword"
    pas2 = "my_pasword2"

    hash_md5 = md5(pas.encode()).hexdigest()
    sha256_md5 = sha256(pas.encode()).hexdigest()
    hash_sha3_512 = sha3_512(pas.encode()).hexdigest()
 
    # print(hash_md5)
    # print(sha256_md5)
    # print(hash_sha3_512)


    crypto = CryptContext(schemes=["sha512_crypt"])

    hash_password1 = crypto.hash(pas)
    hash_password2 = crypto.hash(pas2)



    # print(hash_password1)
    # print(hash_password2)

    # print(hash_password1 == hash_password2) 

    # print(crypto.verify(pas, hash_password2))


    # ЗАДАЧА
    # есть три пароля: w1, w2, w3. Каждый состоит из 6 символов. 
    # Символы - только цифры и латинские буквы в верхнем и нижнем регистрах
    # известно что:
    # md5(w1.encode()).hexdigest() =  b43c7798fdb2ea9e1be9cff35a31080b
    # md5(w2.encode()).hexdigest() =  84d5f8c47297ecbea97337901c757a2b
    # md5(w3.encode()).hexdigest() =  975314b9946a2dde41b1bf480c66f006
    # а также что если:
    # check = word1 + " " + word2 + " " + word3
    # то md5(check.encode()).hexdigest() = 579baeda396e9aba216717750331406b
    # найдите w1, w2, w3.
    # до 23 апреля + 1 команде 


    data = {
        "email": "test@admin.ru",
        "role": "admin",
        "mess": "hello world!!!",
        "exp": int(time.time()) + 3600
    }


    encoded_jwt = jwt.encode(
        data,
        key="i am admin",
        algorithm="HS256",
    )

    print(encoded_jwt)


    payload = jwt.decode(
        encoded_jwt,
        key="i am admin",
        algorithms=["HS256"]
    )


    print(payload)






