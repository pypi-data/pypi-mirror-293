"""
Copyright 2017 Ryan Wick (rrwick@gmail.com)
https://github.com/rrwick/Porechop
This module contains the class and sequences for known adapters used in Oxford Nanopore library
preparation kits.
This file is part of Porechop. Porechop is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by the Free Software Foundation,
either version 3 of the License, or (at your option) any later version. Porechop is distributed in
the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more
details. You should have received a copy of the GNU General Public License along with Porechop. If
not, see <http://www.gnu.org/licenses/>.
"""


class Adapter(object):

    def __init__(self, name, start_sequence=None, end_sequence=None, both_ends_sequence=None):
        self.name = name
        self.start_sequence = start_sequence if start_sequence else []
        self.end_sequence = end_sequence if end_sequence else []
        if both_ends_sequence:
            self.start_sequence = both_ends_sequence
            self.end_sequence = both_ends_sequence
        self.best_start_score, self.best_end_score = 0.0, 0.0

    def best_start_or_end_score(self):
        return max(self.best_start_score, self.best_end_score)

    def is_barcode(self):
        return 'Barcode ' in self.name

    def barcode_direction(self):
        if '_rev' in self.start_sequence[0]:
            return 'reverse'
        else:
            return 'forward'

    def get_barcode_name(self):
        """
        Gets the barcode name for the output files. We want a concise name, so it looks at all
        options and chooses the shortest.
        """
        possible_names = [self.name, self.start_sequence[0]]
        if self.end_sequence:
            possible_names.append(self.end_sequence[0])
        barcode_name = sorted(possible_names, key=lambda x: len(x))[0]
        return barcode_name.replace(' ', '_')


# INSTRUCTIONS FOR ADDING CUSTOM ADAPTERS
# ---------------------------------------
# If you need Porechop to remove adapters that aren't included, you can add your own my modifying
# the ADAPTERS list below.
#
# Here is the format for a normal adapter:
#     Adapter('Adapter_set_name',
#             start_sequence=('Start_adapter_name', 'AAAACCCCGGGGTTTTAAAACCCCGGGGTTTT'),
#             end_sequence=('End_adapter_name', 'AACCGGTTAACCGGTTAACCGGTTAACCGGTT'))
#
# You can exclude start_sequence and end_sequence as appropriate.
#
# If you have custom Barcodes, make sure that the adapter set name starts with 'Barcode '. Also,
# remove the existing barcode sequences from this file to avoid conflicts:
#     Adapter('Barcode 1',
#             start_sequence=('Barcode_1_start', 'AAAAAAAACCCCCCCCGGGGGGGGTTTTTTTT'),
#             end_sequence=('Barcode_1_end', 'AAAAAAAACCCCCCCCGGGGGGGGTTTTTTTT')),
#     Adapter('Barcode 2',
#             start_sequence=('Barcode_2_start', 'TTTTTTTTGGGGGGGGCCCCCCCCAAAAAAAA'),
#             end_sequence=('Barcode_2_end', 'TTTTTTTTGGGGGGGGCCCCCCCCAAAAAAAA'))

NATIVE_BARCODES = [
    # The native barcodes use the rev comp barcode at the start
    # of the read and the forward barcode at the end of the read.
    Adapter('Native Barcode 1',
            start_sequence=('NB01_rev', 'CACAAAGACACCGACAACTTTCTT'),
            end_sequence=('NB01', 'AAGAAAGTTGTCGGTGTCTTTGTG')),
    Adapter('Native Barcode 2',
            start_sequence=('NB02_rev', 'ACAGACGACTACAAACGGAATCGA'),
            end_sequence=('NB02', 'TCGATTCCGTTTGTAGTCGTCTGT')),
    Adapter('Native Barcode 3',
            start_sequence=('NB03_rev', 'CCTGGTAACTGGGACACAAGACTC'),
            end_sequence=('NB03', 'GAGTCTTGTGTCCCAGTTACCAGG')),
    Adapter('Native Barcode 4',
            start_sequence=('NB04_rev', 'TAGGGAAACACGATAGAATCCGAA'),
            end_sequence=('NB04', 'TTCGGATTCTATCGTGTTTCCCTA')),
    Adapter('Native Barcode 5',
            start_sequence=('NB05_rev', 'AAGGTTACACAAACCCTGGACAAG'),
            end_sequence=('NB05', 'CTTGTCCAGGGTTTGTGTAACCTT')),
    Adapter('Native Barcode 6',
            start_sequence=('NB06_rev', 'GACTACTTTCTGCCTTTGCGAGAA'),
            end_sequence=('NB06', 'TTCTCGCAAAGGCAGAAAGTAGTC')),
    Adapter('Native Barcode 7',
            start_sequence=('NB07_rev', 'AAGGATTCATTCCCACGGTAACAC'),
            end_sequence=('NB07', 'GTGTTACCGTGGGAATGAATCCTT')),
    Adapter('Native Barcode 8',
            start_sequence=('NB08_rev', 'ACGTAACTTGGTTTGTTCCCTGAA'),
            end_sequence=('NB08', 'TTCAGGGAACAAACCAAGTTACGT')),
    Adapter('Native Barcode 9',
            start_sequence=('NB09_rev', 'AACCAAGACTCGCTGTGCCTAGTT'),
            end_sequence=('NB09', 'AACTAGGCACAGCGAGTCTTGGTT')),
    Adapter('Native Barcode 10',
            start_sequence=('NB10_rev', 'GAGAGGACAAAGGTTTCAACGCTT'),
            end_sequence=('NB10', 'AAGCGTTGAAACCTTTGTCCTCTC')),
    Adapter('Native Barcode 11',
            start_sequence=('NB11_rev', 'TCCATTCCCTCCGATAGATGAAAC'),
            end_sequence=('NB11', 'GTTTCATCTATCGGAGGGAATGGA')),
    Adapter('Native Barcode 12',
            start_sequence=('NB12_rev', 'TCCGATTCTGCTTCTTTCTACCTG'),
            end_sequence=('NB12', 'CAGGTAGAAAGAAGCAGAATCGGA')),

    Adapter('Native Barcode 13',
            start_sequence=('NB13_rev', 'AGAACGACTTCCATACTCGTGTGA'),
            end_sequence=('NB13', 'TCACACGAGTATGGAAGTCGTTCT')),
    Adapter('Native Barcode 14',
            start_sequence=('NB14_rev', 'AACGAGTCTCTTGGGACCCATAGA'),
            end_sequence=('NB14', 'TCTATGGGTCCCAAGAGACTCGTT')),
    Adapter('Native Barcode 15',
            start_sequence=('NB15_rev', 'AGGTCTACCTCGCTAACACCACTG'),
            end_sequence=('NB15', 'CAGTGGTGTTAGCGAGGTAGACCT')),
    Adapter('Native Barcode 16',
            start_sequence=('NB16_rev', 'CGTCAACTGACAGTGGTTCGTACT'),
            end_sequence=('NB16', 'AGTACGAACCACTGTCAGTTGACG')),
    Adapter('Native Barcode 17',
            start_sequence=('NB17_rev', 'ACCCTCCAGGAAAGTACCTCTGAT'),
            end_sequence=('NB17', 'ATCAGAGGTACTTTCCTGGAGGGT')),
    Adapter('Native Barcode 18',
            start_sequence=('NB18_rev', 'CCAAACCCAACAACCTAGATAGGC'),
            end_sequence=('NB18', 'GCCTATCTAGGTTGTTGGGTTTGG')),
    Adapter('Native Barcode 19',
            start_sequence=('NB19_rev', 'GTTCCTCGTGCAGTGTCAAGAGAT'),
            end_sequence=('NB19', 'ATCTCTTGACACTGCACGAGGAAC')),
    Adapter('Native Barcode 20',
            start_sequence=('NB20_rev', 'TTGCGTCCTGTTACGAGAACTCAT'),
            end_sequence=('NB20', 'ATGAGTTCTCGTAACAGGACGCAA')),
    Adapter('Native Barcode 21',
            start_sequence=('NB21_rev', 'GAGCCTCTCATTGTCCGTTCTCTA'),
            end_sequence=('NB21', 'TAGAGAACGGACAATGAGAGGCTC')),
    Adapter('Native Barcode 22',
            start_sequence=('NB22_rev', 'ACCACTGCCATGTATCAAAGTACG'),
            end_sequence=('NB22', 'CGTACTTTGATACATGGCAGTGGT')),
    Adapter('Native Barcode 23',
            start_sequence=('NB23_rev', 'CTTACTACCCAGTGAACCTCCTCG'),
            end_sequence=('NB23', 'CGAGGAGGTTCACTGGGTAGTAAG')),
    Adapter('Native Barcode 24',
            start_sequence=('NB24_rev', 'GCATAGTTCTGCATGATGGGTTAG'),
            end_sequence=('NB24', 'CTAACCCATCATGCAGAACTATGC'))]

PCR_BARCODES = [
    # Other barcoding kits (like the PCR and rapid barcodes) use the forward barcode at the
    # start of the read and the rev comp barcode at the end of the read.
    Adapter('Barcode 1 (forward)',
            start_sequence=('BC01', 'AAGAAAGTTGTCGGTGTCTTTGTG'),
            end_sequence=('BC01_rev', 'CACAAAGACACCGACAACTTTCTT')),
    Adapter('Barcode 2 (forward)',
            start_sequence=('BC02', 'TCGATTCCGTTTGTAGTCGTCTGT'),
            end_sequence=('BC02_rev', 'ACAGACGACTACAAACGGAATCGA')),
    Adapter('Barcode 3 (forward)',
            start_sequence=('BC03', 'GAGTCTTGTGTCCCAGTTACCAGG'),
            end_sequence=('BC03_rev', 'CCTGGTAACTGGGACACAAGACTC')),
    Adapter('Barcode 4 (forward)',
            start_sequence=('BC04', 'TTCGGATTCTATCGTGTTTCCCTA'),
            end_sequence=('BC04_rev', 'TAGGGAAACACGATAGAATCCGAA')),
    Adapter('Barcode 5 (forward)',
            start_sequence=('BC05', 'CTTGTCCAGGGTTTGTGTAACCTT'),
            end_sequence=('BC05_rev', 'AAGGTTACACAAACCCTGGACAAG')),
    Adapter('Barcode 6 (forward)',
            start_sequence=('BC06', 'TTCTCGCAAAGGCAGAAAGTAGTC'),
            end_sequence=('BC06_rev', 'GACTACTTTCTGCCTTTGCGAGAA')),
    Adapter('Barcode 7 (forward)',
            start_sequence=('BC07', 'GTGTTACCGTGGGAATGAATCCTT'),
            end_sequence=('BC07_rev', 'AAGGATTCATTCCCACGGTAACAC')),
    Adapter('Barcode 8 (forward)',
            start_sequence=('BC08', 'TTCAGGGAACAAACCAAGTTACGT'),
            end_sequence=('BC08_rev', 'ACGTAACTTGGTTTGTTCCCTGAA')),
    Adapter('Barcode 9 (forward)',
            start_sequence=('BC09', 'AACTAGGCACAGCGAGTCTTGGTT'),
            end_sequence=('BC09_rev', 'AACCAAGACTCGCTGTGCCTAGTT')),
    Adapter('Barcode 10 (forward)',
            start_sequence=('BC10', 'AAGCGTTGAAACCTTTGTCCTCTC'),
            end_sequence=('BC10_rev', 'GAGAGGACAAAGGTTTCAACGCTT')),
    Adapter('Barcode 11 (forward)',
            start_sequence=('BC11', 'GTTTCATCTATCGGAGGGAATGGA'),
            end_sequence=('BC11_rev', 'TCCATTCCCTCCGATAGATGAAAC')),
    Adapter('Barcode 12 (forward)',
            start_sequence=('BC12', 'CAGGTAGAAAGAAGCAGAATCGGA'),
            end_sequence=('BC12_rev', 'TCCGATTCTGCTTCTTTCTACCTG')),
    Adapter('Barcode 13 (forward)',
            start_sequence=('BC13', 'AGAACGACTTCCATACTCGTGTGA'),
            end_sequence=('BC13_rev', 'TCACACGAGTATGGAAGTCGTTCT')),
    Adapter('Barcode 14 (forward)',
            start_sequence=('BC14', 'AACGAGTCTCTTGGGACCCATAGA'),
            end_sequence=('BC14_rev', 'TCTATGGGTCCCAAGAGACTCGTT')),
    Adapter('Barcode 15 (forward)',
            start_sequence=('BC15', 'AGGTCTACCTCGCTAACACCACTG'),
            end_sequence=('BC15_rev', 'CAGTGGTGTTAGCGAGGTAGACCT')),
    Adapter('Barcode 16 (forward)',
            start_sequence=('BC16', 'CGTCAACTGACAGTGGTTCGTACT'),
            end_sequence=('BC16_rev', 'AGTACGAACCACTGTCAGTTGACG')),
    Adapter('Barcode 17 (forward)',
            start_sequence=('BC17', 'ACCCTCCAGGAAAGTACCTCTGAT'),
            end_sequence=('BC17_rev', 'ATCAGAGGTACTTTCCTGGAGGGT')),
    Adapter('Barcode 18 (forward)',
            start_sequence=('BC18', 'CCAAACCCAACAACCTAGATAGGC'),
            end_sequence=('BC18_rev', 'GCCTATCTAGGTTGTTGGGTTTGG')),
    Adapter('Barcode 19 (forward)',
            start_sequence=('BC19', 'GTTCCTCGTGCAGTGTCAAGAGAT'),
            end_sequence=('BC19_rev', 'ATCTCTTGACACTGCACGAGGAAC')),
    Adapter('Barcode 20 (forward)',
            start_sequence=('BC20', 'TTGCGTCCTGTTACGAGAACTCAT'),
            end_sequence=('BC20_rev', 'ATGAGTTCTCGTAACAGGACGCAA')),
    Adapter('Barcode 21 (forward)',
            start_sequence=('BC21', 'GAGCCTCTCATTGTCCGTTCTCTA'),
            end_sequence=('BC21_rev', 'TAGAGAACGGACAATGAGAGGCTC')),
    Adapter('Barcode 22 (forward)',
            start_sequence=('BC22', 'ACCACTGCCATGTATCAAAGTACG'),
            end_sequence=('BC22_rev', 'CGTACTTTGATACATGGCAGTGGT')),
    Adapter('Barcode 23 (forward)',
            start_sequence=('BC23', 'CTTACTACCCAGTGAACCTCCTCG'),
            end_sequence=('BC23_rev', 'CGAGGAGGTTCACTGGGTAGTAAG')),
    Adapter('Barcode 24 (forward)',
            start_sequence=('BC24', 'GCATAGTTCTGCATGATGGGTTAG'),
            end_sequence=('BC24_rev', 'CTAACCCATCATGCAGAACTATGC')),
    Adapter('Barcode 25 (forward)',
            start_sequence=('BC25', 'GTAAGTTGGGTATGCAACGCAATG'),
            end_sequence=('BC25_rev', 'CATTGCGTTGCATACCCAACTTAC')),
    Adapter('Barcode 26 (forward)',
            start_sequence=('BC26', 'CATACAGCGACTACGCATTCTCAT'),
            end_sequence=('BC26_rev', 'ATGAGAATGCGTAGTCGCTGTATG')),
    Adapter('Barcode 27 (forward)',
            start_sequence=('BC27', 'CGACGGTTAGATTCACCTCTTACA'),
            end_sequence=('BC27_rev', 'TGTAAGAGGTGAATCTAACCGTCG')),
    Adapter('Barcode 28 (forward)',
            start_sequence=('BC28', 'TGAAACCTAAGAAGGCACCGTATC'),
            end_sequence=('BC28_rev', 'GATACGGTGCCTTCTTAGGTTTCA')),
    Adapter('Barcode 29 (forward)',
            start_sequence=('BC29', 'CTAGACACCTTGGGTTGACAGACC'),
            end_sequence=('BC29_rev', 'GGTCTGTCAACCCAAGGTGTCTAG')),
    Adapter('Barcode 30 (forward)',
            start_sequence=('BC30', 'TCAGTGAGGATCTACTTCGACCCA'),
            end_sequence=('BC30_rev', 'TGGGTCGAAGTAGATCCTCACTGA')),
    Adapter('Barcode 31 (forward)',
            start_sequence=('BC31', 'TGCGTACAGCAATCAGTTACATTG'),
            end_sequence=('BC31_rev', 'CAATGTAACTGATTGCTGTACGCA')),
    Adapter('Barcode 32 (forward)',
            start_sequence=('BC32', 'CCAGTAGAAGTCCGACAACGTCAT'),
            end_sequence=('BC32_rev', 'ATGACGTTGTCGGACTTCTACTGG')),
    Adapter('Barcode 33 (forward)',
            start_sequence=('BC33', 'CAGACTTGGTACGGTTGGGTAACT'),
            end_sequence=('BC33_rev', 'AGTTACCCAACCGTACCAAGTCTG')),
    Adapter('Barcode 34 (forward)',
            start_sequence=('BC34', 'GGACGAAGAACTCAAGTCAAAGGC'),
            end_sequence=('BC34_rev', 'GCCTTTGACTTGAGTTCTTCGTCC')),
    Adapter('Barcode 35 (forward)',
            start_sequence=('BC35', 'CTACTTACGAAGCTGAGGGACTGC'),
            end_sequence=('BC35_rev', 'GCAGTCCCTCAGCTTCGTAAGTAG')),
    Adapter('Barcode 36 (forward)',
            start_sequence=('BC36', 'ATGTCCCAGTTAGAGGAGGAAACA'),
            end_sequence=('BC36_rev', 'TGTTTCCTCCTCTAACTGGGACAT')),
    Adapter('Barcode 37 (forward)',
            start_sequence=('BC37', 'GCTTGCGATTGATGCTTAGTATCA'),
            end_sequence=('BC37_rev', 'TGATACTAAGCATCAATCGCAAGC')),
    Adapter('Barcode 38 (forward)',
            start_sequence=('BC38', 'ACCACAGGAGGACGATACAGAGAA'),
            end_sequence=('BC38_rev', 'TTCTCTGTATCGTCCTCCTGTGGT')),
    Adapter('Barcode 39 (forward)',
            start_sequence=('BC39', 'CCACAGTGTCAACTAGAGCCTCTC'),
            end_sequence=('BC39_rev', 'GAGAGGCTCTAGTTGACACTGTGG')),
    Adapter('Barcode 40 (forward)',
            start_sequence=('BC40', 'TAGTTTGGATGACCAAGGATAGCC'),
            end_sequence=('BC40_rev', 'GGCTATCCTTGGTCATCCAAACTA')),
    Adapter('Barcode 41 (forward)',
            start_sequence=('BC41', 'GGAGTTCGTCCAGAGAAGTACACG'),
            end_sequence=('BC41_rev', 'CGTGTACTTCTCTGGACGAACTCC')),
    Adapter('Barcode 42 (forward)',
            start_sequence=('BC42', 'CTACGTGTAAGGCATACCTGCCAG'),
            end_sequence=('BC42_rev', 'CTGGCAGGTATGCCTTACACGTAG')),
    Adapter('Barcode 43 (forward)',
            start_sequence=('BC43', 'CTTTCGTTGTTGACTCGACGGTAG'),
            end_sequence=('BC43_rev', 'CTACCGTCGAGTCAACAACGAAAG')),
    Adapter('Barcode 44 (forward)',
            start_sequence=('BC44', 'AGTAGAAAGGGTTCCTTCCCACTC'),
            end_sequence=('BC44_rev', 'GAGTGGGAAGGAACCCTTTCTACT')),
    Adapter('Barcode 45 (forward)',
            start_sequence=('BC45', 'GATCCAACAGAGATGCCTTCAGTG'),
            end_sequence=('BC45_rev', 'CACTGAAGGCATCTCTGTTGGATC')),
    Adapter('Barcode 46 (forward)',
            start_sequence=('BC46', 'GCTGTGTTCCACTTCATTCTCCTG'),
            end_sequence=('BC46_rev', 'CAGGAGAATGAAGTGGAACACAGC')),
    Adapter('Barcode 47 (forward)',
            start_sequence=('BC47', 'GTGCAACTTTCCCACAGGTAGTTC'),
            end_sequence=('BC47_rev', 'GAACTACCTGTGGGAAAGTTGCAC')),
    Adapter('Barcode 48 (forward)',
            start_sequence=('BC48', 'CATCTGGAACGTGGTACACCTGTA'),
            end_sequence=('BC48_rev', 'TACAGGTGTACCACGTTCCAGATG')),
    Adapter('Barcode 49 (forward)',
            start_sequence=('BC49', 'ACTGGTGCAGCTTTGAACATCTAG'),
            end_sequence=('BC49_rev', 'CTAGATGTTCAAAGCTGCACCAGT')),
    Adapter('Barcode 50 (forward)',
            start_sequence=('BC50', 'ATGGACTTTGGTAACTTCCTGCGT'),
            end_sequence=('BC50_rev', 'ACGCAGGAAGTTACCAAAGTCCAT')),
    Adapter('Barcode 51 (forward)',
            start_sequence=('BC51', 'GTTGAATGAGCCTACTGGGTCCTC'),
            end_sequence=('BC51_rev', 'GAGGACCCAGTAGGCTCATTCAAC')),
    Adapter('Barcode 52 (forward)',
            start_sequence=('BC52', 'TGAGAGACAAGATTGTTCGTGGAC'),
            end_sequence=('BC52_rev', 'GTCCACGAACAATCTTGTCTCTCA')),
    Adapter('Barcode 53 (forward)',
            start_sequence=('BC53', 'AGATTCAGACCGTCTCATGCAAAG'),
            end_sequence=('BC53_rev', 'CTTTGCATGAGACGGTCTGAATCT')),
    Adapter('Barcode 54 (forward)',
            start_sequence=('BC54', 'CAAGAGCTTTGACTAAGGAGCATG'),
            end_sequence=('BC54_rev', 'CATGCTCCTTAGTCAAAGCTCTTG')),
    Adapter('Barcode 55 (forward)',
            start_sequence=('BC55', 'TGGAAGATGAGACCCTGATCTACG'),
            end_sequence=('BC55_rev', 'CGTAGATCAGGGTCTCATCTTCCA')),
    Adapter('Barcode 56 (forward)',
            start_sequence=('BC56', 'TCACTACTCAACAGGTGGCATGAA'),
            end_sequence=('BC56_rev', 'TTCATGCCACCTGTTGAGTAGTGA')),
    Adapter('Barcode 57 (forward)',
            start_sequence=('BC57', 'GCTAGGTCAATCTCCTTCGGAAGT'),
            end_sequence=('BC57_rev', 'ACTTCCGAAGGAGATTGACCTAGC')),
    Adapter('Barcode 58 (forward)',
            start_sequence=('BC58', 'CAGGTTACTCCTCCGTGAGTCTGA'),
            end_sequence=('BC58_rev', 'TCAGACTCACGGAGGAGTAACCTG')),
    Adapter('Barcode 59 (forward)',
            start_sequence=('BC59', 'TCAATCAAGAAGGGAAAGCAAGGT'),
            end_sequence=('BC59_rev', 'ACCTTGCTTTCCCTTCTTGATTGA')),
    Adapter('Barcode 60 (forward)',
            start_sequence=('BC60', 'CATGTTCAACCAAGGCTTCTATGG'),
            end_sequence=('BC60_rev', 'CCATAGAAGCCTTGGTTGAACATG')),
    Adapter('Barcode 61 (forward)',
            start_sequence=('BC61', 'AGAGGGTACTATGTGCCTCAGCAC'),
            end_sequence=('BC61_rev', 'GTGCTGAGGCACATAGTACCCTCT')),
    Adapter('Barcode 62 (forward)',
            start_sequence=('BC62', 'CACCCACACTTACTTCAGGACGTA'),
            end_sequence=('BC62_rev', 'TACGTCCTGAAGTAAGTGTGGGTG')),
    Adapter('Barcode 63 (forward)',
            start_sequence=('BC63', 'TTCTGAAGTTCCTGGGTCTTGAAC'),
            end_sequence=('BC63_rev', 'GTTCAAGACCCAGGAACTTCAGAA')),
    Adapter('Barcode 64 (forward)',
            start_sequence=('BC64', 'GACAGACACCGTTCATCGACTTTC'),
            end_sequence=('BC64_rev', 'GAAAGTCGATGAACGGTGTCTGTC')),
    Adapter('Barcode 65 (forward)',
            start_sequence=('BC65', 'TTCTCAGTCTTCCTCCAGACAAGG'),
            end_sequence=('BC65_rev', 'CCTTGTCTGGAGGAAGACTGAGAA')),
    Adapter('Barcode 66 (forward)',
            start_sequence=('BC66', 'CCGATCCTTGTGGCTTCTAACTTC'),
            end_sequence=('BC66_rev', 'GAAGTTAGAAGCCACAAGGATCGG')),
    Adapter('Barcode 67 (forward)',
            start_sequence=('BC67', 'GTTTGTCATACTCGTGTGCTCACC'),
            end_sequence=('BC67_rev', 'GGTGAGCACACGAGTATGACAAAC')),
    Adapter('Barcode 68 (forward)',
            start_sequence=('BC68', 'GAATCTAAGCAAACACGAAGGTGG'),
            end_sequence=('BC68_rev', 'CCACCTTCGTGTTTGCTTAGATTC')),
    Adapter('Barcode 69 (forward)',
            start_sequence=('BC69', 'TACAGTCCGAGCCTCATGTGATCT'),
            end_sequence=('BC69_rev', 'AGATCACATGAGGCTCGGACTGTA')),
    Adapter('Barcode 70 (forward)',
            start_sequence=('BC70', 'ACCGAGATCCTACGAATGGAGTGT'),
            end_sequence=('BC70_rev', 'ACACTCCATTCGTAGGATCTCGGT')),
    Adapter('Barcode 71 (forward)',
            start_sequence=('BC71', 'CCTGGGAGCATCAGGTAGTAACAG'),
            end_sequence=('BC71_rev', 'CTGTTACTACCTGATGCTCCCAGG')),
    Adapter('Barcode 72 (forward)',
            start_sequence=('BC72', 'TAGCTGACTGTCTTCCATACCGAC'),
            end_sequence=('BC72_rev', 'GTCGGTATGGAAGACAGTCAGCTA')),
    Adapter('Barcode 73 (forward)',
            start_sequence=('BC73', 'AAGAAACAGGATGACAGAACCCTC'),
            end_sequence=('BC73_rev', 'GAGGGTTCTGTCATCCTGTTTCTT')),
    Adapter('Barcode 74 (forward)',
            start_sequence=('BC74', 'TACAAGCATCCCAACACTTCCACT'),
            end_sequence=('BC74_rev', 'AGTGGAAGTGTTGGGATGCTTGTA')),
    Adapter('Barcode 75 (forward)',
            start_sequence=('BC75', 'GACCATTGTGATGAACCCTGTTGT'),
            end_sequence=('BC75_rev', 'ACAACAGGGTTCATCACAATGGTC')),
    Adapter('Barcode 76 (forward)',
            start_sequence=('BC76', 'ATGCTTGTTACATCAACCCTGGAC'),
            end_sequence=('BC76_rev', 'GTCCAGGGTTGATGTAACAAGCAT')),
    Adapter('Barcode 77 (forward)',
            start_sequence=('BC77', 'CGACCTGTTTCTCAGGGATACAAC'),
            end_sequence=('BC77_rev', 'GTTGTATCCCTGAGAAACAGGTCG')),
    Adapter('Barcode 78 (forward)',
            start_sequence=('BC78', 'AACAACCGAACCTTTGAATCAGAA'),
            end_sequence=('BC78_rev', 'TTCTGATTCAAAGGTTCGGTTGTT')),
    Adapter('Barcode 79 (forward)',
            start_sequence=('BC79', 'TCTCGGAGATAGTTCTCACTGCTG'),
            end_sequence=('BC79_rev', 'CAGCAGTGAGAACTATCTCCGAGA')),
    Adapter('Barcode 80 (forward)',
            start_sequence=('BC80', 'CGGATGAACATAGGATAGCGATTC'),
            end_sequence=('BC80_rev', 'GAATCGCTATCCTATGTTCATCCG')),
    Adapter('Barcode 81 (forward)',
            start_sequence=('BC81', 'CCTCATCTTGTGAAGTTGTTTCGG'),
            end_sequence=('BC81_rev', 'CCGAAACAACTTCACAAGATGAGG')),
    Adapter('Barcode 82 (forward)',
            start_sequence=('BC82', 'ACGGTATGTCGAGTTCCAGGACTA'),
            end_sequence=('BC82_rev', 'TAGTCCTGGAACTCGACATACCGT')),
    Adapter('Barcode 83 (forward)',
            start_sequence=('BC83', 'TGGCTTGATCTAGGTAAGGTCGAA'),
            end_sequence=('BC83_rev', 'TTCGACCTTACCTAGATCAAGCCA')),
    Adapter('Barcode 84 (forward)',
            start_sequence=('BC84', 'GTAGTGGACCTAGAACCTGTGCCA'),
            end_sequence=('BC84_rev', 'TGGCACAGGTTCTAGGTCCACTAC')),
    Adapter('Barcode 85 (forward)',
            start_sequence=('BC85', 'AACGGAGGAGTTAGTTGGATGATC'),
            end_sequence=('BC85_rev', 'GATCATCCAACTAACTCCTCCGTT')),
    Adapter('Barcode 86 (forward)',
            start_sequence=('BC86', 'AGGTGATCCCAACAAGCGTAAGTA'),
            end_sequence=('BC86_rev', 'TACTTACGCTTGTTGGGATCACCT')),
    Adapter('Barcode 87 (forward)',
            start_sequence=('BC87', 'TACATGCTCCTGTTGTTAGGGAGG'),
            end_sequence=('BC87_rev', 'CCTCCCTAACAACAGGAGCATGTA')),
    Adapter('Barcode 88 (forward)',
            start_sequence=('BC88', 'TCTTCTACTACCGATCCGAAGCAG'),
            end_sequence=('BC88_rev', 'CTGCTTCGGATCGGTAGTAGAAGA')),
    Adapter('Barcode 89 (forward)',
            start_sequence=('BC89', 'ACAGCATCAATGTTTGGCTAGTTG'),
            end_sequence=('BC89_rev', 'CAACTAGCCAAACATTGATGCTGT')),
    Adapter('Barcode 90 (forward)',
            start_sequence=('BC90', 'GATGTAGAGGGTACGGTTTGAGGC'),
            end_sequence=('BC90_rev', 'GCCTCAAACCGTACCCTCTACATC')),
    Adapter('Barcode 91 (forward)',
            start_sequence=('BC91', 'GGCTCCATAGGAACTCACGCTACT'),
            end_sequence=('BC91_rev', 'AGTAGCGTGAGTTCCTATGGAGCC')),
    Adapter('Barcode 92 (forward)',
            start_sequence=('BC92', 'TTGTGAGTGGAAAGATACAGGACC'),
            end_sequence=('BC92_rev', 'GGTCCTGTATCTTTCCACTCACAA')),
    Adapter('Barcode 93 (forward)',
            start_sequence=('BC93', 'AGTTTCCATCACTTCAGACTTGGG'),
            end_sequence=('BC93_rev', 'CCCAAGTCTGAAGTGATGGAAACT')),
    Adapter('Barcode 94 (forward)',
            start_sequence=('BC94', 'GATTGTCCTCAAACTGCCACCTAC'),
            end_sequence=('BC94_rev', 'GTAGGTGGCAGTTTGAGGACAATC')),
    Adapter('Barcode 95 (forward)',
            start_sequence=('BC95', 'CCTGTCTGGAAGAAGAATGGACTT'),
            end_sequence=('BC95_rev', 'AAGTCCATTCTTCTTCCAGACAGG')),
    Adapter('Barcode 96 (forward)',
            start_sequence=('BC96', 'CTGAACGGTCATAGAGTCCACCAT'),
            end_sequence=('BC96_rev', 'ATGGTGGACTCTATGACCGTTCAG'))]

RAPID_BARCODES = [
    Adapter('Rapid Barcode 1 (reverse)',
            start_sequence=('BC01', 'AAGAAAGTTGTCGGTGTCTTTGTG')),
    Adapter('Rapid Barcode 2 (reverse)',
            start_sequence=('BC02', 'TCGATTCCGTTTGTAGTCGTCTGT')),
    Adapter('Rapid Barcode 3 (reverse)',
            start_sequence=('BC03', 'GAGTCTTGTGTCCCAGTTACCAGG')),
    Adapter('Rapid Barcode 4 (reverse)',
            start_sequence=('BC04', 'TTCGGATTCTATCGTGTTTCCCTA')),
    Adapter('Rapid Barcode 5 (reverse)',
            start_sequence=('BC05', 'CTTGTCCAGGGTTTGTGTAACCTT')),
    Adapter('Rapid Barcode 6 (reverse)',
            start_sequence=('BC06', 'TTCTCGCAAAGGCAGAAAGTAGTC')),
    Adapter('Rapid Barcode 7 (reverse)',
            start_sequence=('BC07', 'GTGTTACCGTGGGAATGAATCCTT')),
    Adapter('Rapid Barcode 8 (reverse)',
            start_sequence=('BC08', 'TTCAGGGAACAAACCAAGTTACGT')),
    Adapter('Rapid Barcode 9 (reverse)',
            start_sequence=('BC09', 'AACTAGGCACAGCGAGTCTTGGTT')),
    Adapter('Rapid Barcode 10 (reverse)',
            start_sequence=('BC10', 'AAGCGTTGAAACCTTTGTCCTCTC')),
    Adapter('Rapid Barcode 11 (reverse)',
            start_sequence=('BC11', 'GTTTCATCTATCGGAGGGAATGGA')),
    Adapter('Rapid Barcode 12 (reverse)',
            start_sequence=('BC12', 'CAGGTAGAAAGAAGCAGAATCGGA')),
]

OTHER_ADAPTERS = [
    Adapter('Barcode 13 (reverse)',
            start_sequence=('BC13', 'AGAACGACTTCCATACTCGTGTGA'),
            end_sequence=('BC13_rev', 'TCACACGAGTATGGAAGTCGTTCT')),
    Adapter('Barcode 14 (reverse)',
            start_sequence=('BC14', 'AACGAGTCTCTTGGGACCCATAGA'),
            end_sequence=('BC14_rev', 'TCTATGGGTCCCAAGAGACTCGTT')),
    Adapter('Barcode 15 (reverse)',
            start_sequence=('BC15', 'AGGTCTACCTCGCTAACACCACTG'),
            end_sequence=('BC15_rev', 'CAGTGGTGTTAGCGAGGTAGACCT')),
    Adapter('Barcode 16 (reverse)',
            start_sequence=('BC16', 'CGTCAACTGACAGTGGTTCGTACT'),
            end_sequence=('BC16_rev', 'AGTACGAACCACTGTCAGTTGACG')),
    Adapter('Barcode 17 (reverse)',
            start_sequence=('BC17', 'ACCCTCCAGGAAAGTACCTCTGAT'),
            end_sequence=('BC17_rev', 'ATCAGAGGTACTTTCCTGGAGGGT')),
    Adapter('Barcode 18 (reverse)',
            start_sequence=('BC18', 'CCAAACCCAACAACCTAGATAGGC'),
            end_sequence=('BC18_rev', 'GCCTATCTAGGTTGTTGGGTTTGG')),
    Adapter('Barcode 19 (reverse)',
            start_sequence=('BC19', 'GTTCCTCGTGCAGTGTCAAGAGAT'),
            end_sequence=('BC19_rev', 'ATCTCTTGACACTGCACGAGGAAC')),
    Adapter('Barcode 20 (reverse)',
            start_sequence=('BC20', 'TTGCGTCCTGTTACGAGAACTCAT'),
            end_sequence=('BC20_rev', 'ATGAGTTCTCGTAACAGGACGCAA')),
    Adapter('Barcode 21 (reverse)',
            start_sequence=('BC21', 'GAGCCTCTCATTGTCCGTTCTCTA'),
            end_sequence=('BC21_rev', 'TAGAGAACGGACAATGAGAGGCTC')),
    Adapter('Barcode 22 (reverse)',
            start_sequence=('BC22', 'ACCACTGCCATGTATCAAAGTACG'),
            end_sequence=('BC22_rev', 'CGTACTTTGATACATGGCAGTGGT')),
    Adapter('Barcode 23 (reverse)',
            start_sequence=('BC23', 'CTTACTACCCAGTGAACCTCCTCG'),
            end_sequence=('BC23_rev', 'CGAGGAGGTTCACTGGGTAGTAAG')),
    Adapter('Barcode 24 (reverse)',
            start_sequence=('BC24', 'GCATAGTTCTGCATGATGGGTTAG'),
            end_sequence=('BC24_rev', 'CTAACCCATCATGCAGAACTATGC')),
    Adapter('SQK-NSK007',
            start_sequence=('SQK-NSK007_Y_Top', 'AATGTACTTCGTTCAGTTACGTATTGCT'),
            end_sequence=('SQK-NSK007_Y_Bottom', 'GCAATACGTAACTGAACGAAGT')),

    Adapter('Rapid',
            start_sequence=('Rapid_adapter', 'GTTTTCGCATTTATCGTGAAACGCTTTCGCGTTTTTCGTGCGCCGCTTCA')),

    Adapter('SQK-MAP006',
            start_sequence=('SQK-MAP006_Y_Top_SK63',    'GGTTGTTTCTGTTGGTGCTGATATTGCT'),
            end_sequence=  ('SQK-MAP006_Y_Bottom_SK64', 'GCAATATCAGCACCAACAGAAA')),

    Adapter('SQK-MAP006 Short',
            start_sequence=('SQK-MAP006_Short_Y_Top_LI32',    'CGGCGTCTGCTTGGGTGTTTAACCT'),
            end_sequence=  ('SQK-MAP006_Short_Y_Bottom_LI33', 'GGTTAAACACCCAAGCAGACGCCG')),

    Adapter('PCR adapters 1',
            start_sequence=('PCR_1_start', 'ACTTGCCTGTCGCTCTATCTTC'),
            end_sequence=  ('PCR_1_end', 'GAAGATAGAGCGACAGGCAAGT')),

    Adapter('PCR tail 1',
            start_sequence=('PCR_tail_1_start', 'TTAACCTTTCTGTTGGTGCTGATATTGC'),
            end_sequence=  ('PCR_tail_1_end',   'GCAATATCAGCACCAACAGAAAGGTTAA')),

    Adapter('PCR tail 2',
            start_sequence=('PCR_tail_2_start', 'TTAACCTACTTGCCTGTCGCTCTATCTTC'),
            end_sequence=  ('PCR_tail_2_end',   'GAAGATAGAGCGACAGGCAAGTAGGTTAA')),


    # 1D^2 kit adapters are interesting. ONT provided the following sequences on their site:
    #   start: GGCGTCTGCTTGGGTGTTTAACCTTTTTGTCAGAGAGGTTCCAAGTCAGAGAGGTTCCT
    #   end:   GGAACCTCTCTCTGACTTGGAACCTCTCTGACAAAAAGGTTAAACACCCAAGCAGACGCCAGCAAT
    # But when looking at actual reads, I found two parts. The first corresponds to one end
    # of the provided sequences (through slightly different):
    Adapter('1D^2 part 1',
            start_sequence=('1D2_part_1_start', 'GAGAGGTTCCAAGTCAGAGAGGTTCCT'),
            end_sequence=  ('1D2_part_1_end',   'AGGAACCTCTCTGACTTGGAACCTCTC')),
    # and the second part corresponds to the other end, combined with a bit of standard 1D
    # adapter:
    Adapter('1D^2 part 2',
            start_sequence=('1D2_part_2_start', 'CTTCGTTCAGTTACGTATTGCTGGCGTCTGCTT'),
            end_sequence=  ('1D2_part_2_end',   'CACCCAAGCAGACGCCAGCAATACGTAACT')),
    # The middle part of the provided sequences is less common, so I've left it out of the
    # adapter sequences here.
    ]

ALL_ADAPTERS = NATIVE_BARCODES + PCR_BARCODES + RAPID_BARCODES + OTHER_ADAPTERS


def make_full_native_barcode_adapter(barcode_num):
    barcode = [x for x in NATIVE_BARCODES if x.name == 'Native Barcode ' + str(barcode_num)][0]
    start_barcode_seq = barcode.start_sequence[1]
    end_barcode_seq = barcode.end_sequence[1]

    start_full_seq = 'AATGTACTTCGTTCAGTTACGTATTGCTAAGGTTAA' + start_barcode_seq + 'CAGCACCT'
    end_full_seq = 'AGGTGCTG' + end_barcode_seq + 'TTAACCTTAGCAATACGTAACTGAACGAAGT'

    return Adapter('Native barcoding ' + str(barcode_num) + ' (full sequence)',
                   start_sequence=('NB' + '%02d' % barcode_num + '_start', start_full_seq),
                   end_sequence=('NB' + '%02d' % barcode_num + '_end', end_full_seq))


def make_full_rapid_barcode_adapter(barcode_num):
    barcode = [x for x in ALL_ADAPTERS if x.name == 'Barcode ' + str(barcode_num) + ' (forward)'][0]
    start_barcode_seq = barcode.start_sequence[1]

    start_full_seq = 'AATGTACTTCGTTCAGTTACGTATTGCT' + start_barcode_seq + 'GTTTTCGCATTTATCGTGAAACGCTTTCGCGTTTTTCGTGCGCCGCTTCA'

    return Adapter('Rapid barcoding ' + str(barcode_num) + ' (full sequence)',
                   start_sequence=('RB' + '%02d' % barcode_num + '_full', start_full_seq))

def load_primers(primer_file):
    c = 0
    # file should be csv eg:
    # primer1_LEFT,seq\n
    # primer1_right,seq\n
    # primer2_LEFT,seq\n
    # primer2_right,seq\n

    print("Loading primers from file {}...".format(primer_file))
    CUSTOM_BARCODES=[]
    start_name=''
    end_name=''
    name=''
    custom_barcodes = str(primer_file)
    with open(custom_barcodes,"r") as f:
        for l in f:
            c +=1
            tokens=l.split(',')
            if c%2!=0:
                name='Barcode {} (forward)'.format(tokens[0].rstrip('_LEFT'))
                start_name=tokens[0]
                start_seq=tokens[1]
            else:
                if name=='Barcode {} (forward)'.format(tokens[0].rstrip('_RIGHT')):
                    end_name=tokens[0]
                    end_seq=tokens[1]
                    print(name, start_name, end_name, start_seq, end_seq)
                    CUSTOM_BARCODES.append(Adapter(name, start_sequence=(start_name, start_seq), end_sequence=(end_name, end_seq)))
    return CUSTOM_BARCODES

def load_custom_barcodes(custom_barcode_file):
    c = 0
    # file should be csv with columns [Name,Direction{1=Forward,0=Reverse},StartSeq,EndSeq]
    print("Loading custom barcodes from file {}...".format(custom_barcode_file))
    CUSTOM_BARCODES=[]
    start_name=''
    end_name=''
    name=''
    custom_barcodes = str(custom_barcode_file)
    barcode_dict = {}
    with open(custom_barcodes,"r") as f:
        for l in f:
            if l.startswith("#"):
                continue
            c +=1
            tokens=l.split(',')
            name=tokens[0]
            direction = tokens[1]
            if direction:
                ad_name=name + ' (forward)'
                end_name=name+'_rev'
                CUSTOM_BARCODES.append(Adapter(ad_name, start_sequence=(name, tokens[2]), end_sequence=(end_name, tokens[3])))
            else:
                ad_name=name + ' (reverse)'
                start_name=name+'_rev'
                CUSTOM_BARCODES.append(Adapter(ad_name, start_sequence=(start_name, tokens[2]), end_sequence=(name, tokens[3])))
    return CUSTOM_BARCODES
