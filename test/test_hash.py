from passlib.hash import pbkdf2_sha512

my_input = input("输入密码进行加密")
hash = pbkdf2_sha512.hash(my_input)

print(hash)
print(pbkdf2_sha512.verify("youtube", hash))

last_hash="$pbkdf2-sha512$25000$kNKaU.p9r1VKKWVMKeWc8w$jj17O/cbAuUqIJjlNaM5ZP2x8I7SsNReZd9/kzNEW9AUV3ZbJMx0.4qGuSokqEj3ryD1/cK5LLuUeu0f/SxI4w"

print(pbkdf2_sha512.verify("youtube", last_hash))