from cryptography.fernet import Fernet


class URLEnDecrypt:
    # todo: key -> sercret file로 이동
    fern = Fernet(b'-LEZDdGOWGRYilzx0OGbROixG5ImgjGY40MhS0AHgNA=')

    @classmethod
    def encrypt(cls, text):
        enc_data = cls.fern.encrypt(text.encode('utf-8'))
        return enc_data.decode('utf-8')

    @classmethod
    def decrypt(cls, text):
        dec_data = cls.fern.decrypt(text.encode('utf-8'))
        return dec_data.decode('utf-8')
