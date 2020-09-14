# from datetime import timedelta
# from django.core.signing import TimestampSigner
#
# signer = TimestampSigner()
# value = signer.sign(('hi'))  # encrypt the PK.
# print(value)
# value = value.replace('hi', "")  # doing this because, it append the original primary key + encrypted string.
# print(value)
# repack = "{}:{}".format('hi', value)  # When you want back the original PK, add the PK + encrypted string.
# dec = signer.unsign(repack)  # decrypt the PK.
# print(dec)

