#!/usr/bin/env python3

import sys
from datetime import UTC, datetime
from pathlib import Path
from subprocess import run

from cryptography.hazmat.primitives.hashes import SHA256
from cryptography.hazmat.primitives.serialization import Encoding
from cryptography.x509 import Certificate, load_pem_x509_certificate

DISTRUSTED = (
    # Symantec
    "FF856A2D251DCD88D36656F450126798CFABAADE40799C722DE4D2B5DB36A73A",
    "37D51006C512EAAB626421F1EC8C92013FC5F82AE98EE533EB4619B8DEB4D06C",
    "5EDB7AC43B82A06A8761E8D7BE4979EBF2611F7DD79BF91C1C6B566A219ED766",
    "B478B812250DF878635C2AA7EC7D155EAA625EE82916E2CD294361886CD1FBD4",
    "A0459B9F63B22559F5FA5D4C6DB3F9F72FF19342033578F073BF1D1B46CBB912",
    "8D722F81A9C113C0791DF136A2966DB26C950A971DB46B4199F4EA54B78BFB9F",
    "A4310D50AF18A6447190372A86AFAF8B951FFB431D837F1E5688B45971ED1557",
    "4B03F45807AD70F21BFC2CAE71C9FDE4604C064CF5FFB686BAE5DBAAD7FDD34C",
    "3F9F27D583204B9E09C8A3D2066C4B57D3A2479C3693650880505698105DBCE9",
    "3A43E220FE7F3EA9653D1E21742EAC2B75C20FD8980305BC502CAF8C2D9B41A1",
    "A4B6B3996FC2F306B3FD8681BD63413D8C5009CC4FA329C2CCF0E2FA1B140305",
    "83CE3C1229688A593D485F81973C0F9195431EDA37CC5E36430E79C7A888638B",
    "EB04CF5EB1F39AFA762F2BB120F296CBA520C1B97DB1589565B81CB9A17B7244",
    "69DDD7EA90BB57C93E135DC85EA6FCD5480B603239BDC454FC758B2A26CF7F79",
    "9ACFAB7E43C8D880D06B262A94DEEEE4B4659989C3D0CAF19BAF6405E41AB7DF",
    "2399561127A57125DE8CEFEA610DDF2FA078B5C8067F4E828290BFB860E84B3C",
    # Entrust
    "73C176434F1BC6D5ADF45B0E76E727287C8DE57616C1E6E6141A2B2CBC7D8E4C",
    "02ED0EB28C14DA45165C566791700D6451D7FB56F0B2AB1D3B8EB070E56EDFF5",
    "43DF5774B03E7FEF5FE40D931A7BEDF1BB2E6B42738C4E6D3841103D3AA7F339",
    "DB3517D1F6732A2D5AB97C533EC70779EE3270A62FB4AC4238372460E6F01E88",
    "6DC47172E01CBCB0BF62580D895FE2B8AC9AD4F873801E0C10B9C837D21EB177",
    "0376AB1D54C5F9803CE4B2E201A0EE7EEF7B57B636E8A93C9B8D4860C96F5FA7",
    "0A81EC5A929777F145904AF38D5D509F66B5E2C58FCDB531058B0E17F3F0B41B",
    "70A73F7F376B60074248904534B11482D5BF0E698ECC498DF52577EBF2E93B9A",
    "BD71FDF6DA97E4CF62D1647ADD2581B07D79ADF8397EB4ECBA9C5E8488821423",
    # Camerfirma
    "0C258A12A5674AEF25F28BA7DCFAECEEA348E541E6F5CC4EE63B71B361606AC3",
    "063E4AFAC491DFD332F3089B8542E94617D893D7FE944E10A7937EE29D9693C0",
    "136335439334A7698016A0D324DE72284E079D7B5220BB8FBD747816EEBEBACA",

    # Not trusted by Mozilla:

    # CN=Certum CA,O=Unizeto Sp. z o.o.,C=PL
    "D8E0FEBC1DB2E38D00940F37D27D41344D993E734B99D5656D9778D4D8143624",
    # CN=DigiCert CS ECC P384 Root G5,O=DigiCert\, Inc.,C=US
    "26C56AD2208D1E9B152F66853BF4797CBEB7552C1F3F477251E8CB1AE7E797BF",
    # CN=DigiCert CS RSA4096 Root G5,O=DigiCert\, Inc.,C=US
    "7353B6D6C2D6DA4247773F3F07D075DECB5134212BEAD0928EF1F46115260941",
    # CN=GlobalSign,O=GlobalSign,OU=GlobalSign ECC Root CA - R4
    "BEC94911C2955676DB6C0A550986D76E3BA005667C442C9762B4FBB773DE228C",
    # CN=LuxTrust Global Root 2,O=LuxTrust S.A.,C=LU
    "54455F7129C20B1447C418F997168F24C58FC5023BF5DA5BE2EB6E1DD8902ED5",
    # CN=SwissSign Platinum CA - G2,O=SwissSign AG,C=CH
    "3B222E566711E992300DC0B15AB9473DAFDEF8C84D0CEF7D3317B4C1821D1436",
    # CN=emSign Root CA - G2,O=eMudhra Technologies Limited,OU=emSign PKI,C=IN
    "1AA0C2709E831BD6E3B5129A00BA41F7EEEF020872F1E6504BF0F6C3F24F3AF3",
)


def main() -> None:
    certs: list[Certificate] = []
    for path in Path(sys.argv[1]).iterdir():
        if path.name == "README":
            continue
        certs.append(load_pem_x509_certificate(path.read_bytes()))
    for cert in sorted(certs, key=lambda c: c.subject.rfc4514_string()):
        if cert.fingerprint(SHA256()).hex().upper() in DISTRUSTED:
            continue
        if cert.not_valid_after_utc < datetime.now(UTC):
            continue
        pem = cert.public_bytes(Encoding.PEM)
        print(cert.subject.rfc4514_string(), file=sys.stderr)
        run(("openssl", "x509", "-text"), check=True, input=pem)
        print(flush=True)


if __name__ == "__main__":
    main()
