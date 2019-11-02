#!/usr/bin/env python
# -*- coding: utf8 -*-
#
#  pyimg4 A python lib for manipulating IMG4, IM4M and IM4P files.
#
# Copyright (c) 2017 "dark[-at-]gotohack.org"
#
#
# pymobiledevice is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
#import sys
from scapy.asn1packet import *
from scapy.asn1fields import *
from scapy.layers.x509 import *
from scapy.asn1.mib import conf
from scapy.layers.x509 import _PacketFieldRaw
from pprint import *

from scapy.asn1.asn1 import ASN1_Class_UNIVERSAL, ASN1_BIT_STRING, ASN1Tag, ASN1_Class


class KBAG(ASN1_Packet):
    ASN1_codec = ASN1_Codecs.BER
    ASN1_root =  ASN1F_SEQUENCE(
                        ASN1F_INTEGER("ID",None),
                        ASN1F_STRING("IV",""),
                        ASN1F_STRING("KEY","")
                    )



class MANP(ASN1_Packet):
    ASN1_codec = ASN1_Codecs.BER
    ASN1_root =  ASN1F_SEQUENCE(
                    ASN1F_IA5_STRING("NAME", ""),
                    ASN1F_CHOICE("VALUE", ASN1F_IA5_STRING, ASN1F_STRING, ASN1F_BOOLEAN, ASN1F_INTEGER),
                    #ASN1F_IA5_STRING("DATA", "", flexible_tag=True), #FIXME
                    explicit_tag=0x04,
                    flexible_tag=True
    )

    def post_dissection(self, p):
        if p.NAME:
            self.name = str(p.NAME)
        return p


class TAG(ASN1_Packet):
    ASN1_codec = ASN1_Codecs.BER
    ASN1_root =  ASN1F_SEQUENCE(
                    ASN1F_IA5_STRING("TYPE", ""),
                    ASN1F_SET_OF("DATA", [MANP()], MANP),
                    explicit_tag=0x04,
                    flexible_tag=True
    )

    def post_dissection(self, p):
        if p.TYPE:
            self.name = str(p.TYPE)
        return p


class MAMB(ASN1_Packet):
    ASN1_codec = ASN1_Codecs.BER
    ASN1_root =  ASN1F_SEQUENCE(
                    ASN1F_IA5_STRING("TYPE", ""),
                    ASN1F_SET_OF("DATA", [TAG()], TAG),
                    explicit_tag=0x04,
                    flexible_tag=True
                )
    #def post_dissection(self, p):
    #    if p.TYPE:
    #        self.name = str(p.TYPE)
    #    return p


class IM4M(ASN1_Packet):
    ASN1_codec = ASN1_Codecs.BER
    ASN1_root = ASN1F_SEQUENCE(
                    ASN1F_IA5_STRING("MAGIC", "IM4M"),
                    ASN1F_INTEGER("VERSION", 0),
                    ASN1F_SET_OF("DATA", [MAMB()], MAMB),
                    ASN1F_optional(ASN1F_STRING("SIGNATURE",None)),
                    ASN1F_optional(ASN1F_SEQUENCE_OF("CERTIFICATES", None, X509_Cert)),
                )
    def post_dissection(self, p):
        if p.MAGIC:
            self.name = str(p.MAGIC)
        return p


class IM4P(ASN1_Packet):
    ASN1_codec = ASN1_Codecs.BER
    ASN1_root = ASN1F_SEQUENCE(
                    ASN1F_IA5_STRING("MAGIC", "IM4P"),
                    ASN1F_IA5_STRING("TYPE", ""),
                    ASN1F_IA5_STRING("DESCRIPTION", ""),
                    ASN1F_STRING("DATA", ""),
                    ASN1F_optional(ASN1F_SEQUENCE_OF("KBAG", None, KBAG, explicit_tag=0x04)),
    )


class IMG4(ASN1_Packet):
    ASN1_codec = ASN1_Codecs.BER
    ASN1_root = ASN1F_SEQUENCE(
        ASN1F_IA5_STRING("MAGIC", "IMG4"),
        ASN1F_PACKET("IM4P",IM4P(),IM4P), #FIXME
        ASN1F_PACKET("IM4M", IM4M(), IM4M, explicit_tag=0xa0),
    )


class X509_ExtIMG4Statement(ASN1_Packet):
    ASN1_codec = ASN1_Codecs.BER
    ASN1_root = ASN1F_SET_OF("TAG", [TAG()], TAG, explicit_tag=0x04)


#ext_mapping["1.2.840.113635.100.6.1.15"] = X509_ExtIMG4Statement

def main():
    args = sys.argv[1:]
    if len(args) != 2:
        print "%s <infile> <outfile>" % sys.argv[0]
        return -1

    with open(args[1], 'w+') as outfile:
        with open(args[0], 'rb') as infile:
            i =  IMG4(infile.read())
            i.show()
            outfile.write(str(i.IM4P.DATA))
    return 0

if __name__ == "__main__":
    exit(main())

