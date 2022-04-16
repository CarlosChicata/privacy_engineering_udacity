#
# This file contains classes that correspond to voters
#

from enum import Enum
from Cryptodome.Cipher import AES
from Crypto.Random import get_random_bytes
from base64 import b64encode, b64decode


NAME_ENCRYPTION_KEY = get_random_bytes(32)
MAPPER = dict()

def obfuscate_national_id(national_id: str) -> str:
    """
    Minimizes a national ID. The minimization may be either irreversible or reversible, but one might make life easier
    that the other, depending on the use-cases.

    :param: national_id A real national ID that is sensitive and needs to be obfuscated in some manner.
    :return: An obfuscated version of the national_id.
    """
    sanitized_national_id = national_id.replace("-", "").replace(" ", "").strip()
    try:
        if len(sanitized_national_id) >= 5:
            return sanitized_national_id[0] + "***" + sanitized_national_id[-1]
        else:
            return "*****"
    except Exception as e:
        raise e


def encrypt_name(name: str) -> str:
    """
    Encrypts a name, non-deterministically.

    :param: name A plaintext name that is sensitive and needs to encrypt.
    :return: The encrypted cipher text of the name.
    """
    try:
        random_value = b64encode(get_random_bytes(16)).decode("utf-8")
        name = name
        cipher = AES.new(
            NAME_ENCRYPTION_KEY, 
            mode=AES.MODE_EAX
        )
        ciphertext = cipher.encrypt(name.encode("utf-8"))
        ciphertext = b64encode(ciphertext).decode("utf-8")
        MAPPER[ciphertext] = (
            random_value, 
            None,
            cipher.nonce
        )
        return ciphertext
    except Exception as e:
        raise e;


def decrypt_name(encrypted_name: str) -> str:
    """
    Decrypts a name. This is the inverse of the encrypt_name method above.

    :param: encrypted_name The ciphertext of a name that is sensitive
    :return: The plaintext name
    """
    try:
        tuple = MAPPER.get(encrypted_name) or (None, None)
        cipher = AES.new(
            NAME_ENCRYPTION_KEY, 
            mode=AES.MODE_EAX,
            nonce=tuple[2]
        )
        ciphertext = cipher.decrypt(
            b64decode(encrypted_name)
        )
        ciphertext = ciphertext.decode("utf-8")
        return ciphertext
    except Exception as e:
        raise e;



class MinimalVoter:
    """
    Our representation of a voter, with the national id obfuscated (but still unique).
    This is the class that we want to be using in the majority of our codebase.
    """
    def __init__(self, obfuscated_first_name: str, obfuscated_last_name: str, obfuscated_national_id: str):
        self.obfuscated_national_id = obfuscated_national_id
        self.obfuscated_first_name = obfuscated_first_name
        self.obfuscated_last_name = obfuscated_last_name


class Voter:
    """
    Our representation of a voter, including certain sensitive information.=
    This class should only be used in the initial stages when requests come in; in the rest of the
    codebase, we should be using the ObfuscatedVoter class
    """
    def __init__(self, first_name: str, last_name: str, national_id: str):
        self.national_id = national_id
        self.first_name = first_name
        self.last_name = last_name

    def get_minimal_voter(self) -> MinimalVoter:
        """
        Converts this object (self) into its obfuscated version
        """
        return MinimalVoter(
            encrypt_name(self.first_name.strip()),
            encrypt_name(self.last_name.strip()),
            obfuscate_national_id(self.national_id))


class VoterStatus(Enum):
    """
    An enum that represents the current status of a voter.
    """
    NOT_REGISTERED = "not registered"
    REGISTERED_NOT_VOTED = "registered, but no ballot received"
    BALLOT_COUNTED = "ballot counted"
    FRAUD_COMMITTED = "fraud committed"


class BallotStatus(Enum):
    """
    An enum that represents the current status of a voter.
    """
    VOTER_BALLOT_MISMATCH = "the ballot doesn't belong to the voter specified"
    INVALID_BALLOT = "the ballot given is invalid"
    FRAUD_COMMITTED = "fraud committed: the voter has already voted"
    VOTER_NOT_REGISTERED = "voter not registered"
    BALLOT_COUNTED = "ballot counted"


