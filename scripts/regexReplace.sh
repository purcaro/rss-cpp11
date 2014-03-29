#!/bin/bash



#define UBYTE unsigned char       /* Wants to be unsigned 8 bits. */
#define BYTE signed char          /* Wants to be signed 8 bits. */
#define UWORD unsigned short      /* Wants to be unsigned 16 bits. */
#define WORD short                /* Wants to be signed 16 bits. */
#define bits64 unsigned long long /* Wants to be unsigned 64 bits. */
#define bits32 unsigned           /* Wants to be unsigned 32 bits. */
#define bits16 unsigned short     /* Wants to be unsigned 16 bits. */
#define bits8 unsigned char       /* Wants to be unsigned 8 bits. */
#define signed32 int              /* Wants to be signed 32 bits. */
#define bits8 unsigned char       /* Wants to be unsigned 8 bits. */


find ~/weng-lab/bigWig/src | xargs -i perl -p -i -e 's/UBYTE/uint8_t/g' {}
find ~/weng-lab/bigWig/src | xargs -i perl -p -i -e 's/BYTE/int8_t/g' {}
find ~/weng-lab/bigWig/src | xargs -i perl -p -i -e 's/UWORD/uint16_t/g' {}
find ~/weng-lab/bigWig/src | xargs -i perl -p -i -e 's/WORD/int16_t/g' {}
find ~/weng-lab/bigWig/src | xargs -i perl -p -i -e 's/bits64/uint64_t/g' {}
find ~/weng-lab/bigWig/src | xargs -i perl -p -i -e 's/bits32/uint32_t/g' {}
find ~/weng-lab/bigWig/src | xargs -i perl -p -i -e 's/bits16/uint16_t/g' {}
find ~/weng-lab/bigWig/src | xargs -i perl -p -i -e 's/bits8/uint8_t/g' {}
find ~/weng-lab/bigWig/src | xargs -i perl -p -i -e 's/signed32/int32_t/g' {}
find ~/weng-lab/bigWig/src | xargs -i perl -p -i -e 's/bits8/uint8_t/g' {}
