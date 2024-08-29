class Akc: #this class replaces the original namespace 'Akc'
    class Bitwise:
        _Bits32Count_mask = { 0x55555555, 0x33333333, 0x0F0F0F0F, 0x00FF00FF, 0x0000FFFF }

        @staticmethod
        def BitMaxValue(x):
            x |= x >> 1
            x |= x >> 2
            x |= x >> 4
            x |= x >> 8
            x |= x >> 16
            return x & ~(x >> 1)

        @staticmethod
        def BitMaxValue2(x):
            x |= x >> 1
            x |= x >> 2
            x |= x >> 4
            x |= x >> 8
            x |= x >> 16
            return x - (x >> 1)

        @staticmethod
        def BitMinValue(x):
            return x & (~x + 1)

        @staticmethod
        def LeastSigBitSet(value):
            return value & 0 - value

        @staticmethod
        def LeastSigBitSet(value):
            return value & -value

        @staticmethod
        def BitMinValue(x):
            return x & (~x + 1)

        @staticmethod
        def BitCount(value):
            count = 0
            while value != 0:
                count += 1
                value &= value - 1
            return count

        @staticmethod
        def BitCount(value):
            count = 0
            while value != 0:
                count += 1
                value &= value - 1
            return count

        @staticmethod
        def BitCount2(x):
            i = None
            shift = None
            i = 0
            shift = 1
            while i < 5:
                x = (x & Akc.Bitwise._Bits32Count_mask[i]) + ((x >> shift) & Akc.Bitwise._Bits32Count_mask[i])
                i += 1
                shift *= 2
            return int(x)

        @staticmethod
        def ByteCount(value):
            _value = value.AsULong()

            count = 0
            while _value != 0:
                count += 1
                _value = _value >> 8
            return count

        #}
        #    //Send(buffer, 4)
        #    //buffer[3] = (byte)((data >> 24) & 0xFF)
        #    //buffer[2] = (byte)((data >> 16) & 0xFF)
        #    //buffer[1] = (byte)((data >> 8) & 0xFF)
        #    //buffer[0] = (byte)(data & 0xFF)

        #    //byte* buffer = stackalloc byte[4]
        #   byte* buffer = stackalloc byte[16]
        #{
        #private static unsafe Byte16 Send(this uint data)

#C# TO PYTHON CONVERTER TODO TASK: There is no preprocessor in Python:
        ##region metot

        # mod 255
        @staticmethod
        def WORDBITS(x):
            return (x * 0x01010101) >> 24

        @staticmethod
        def lzc(x):
            x |= x >> 1
            x |= x >> 2
            x |= x >> 4
            x |= x >> 8
            x |= x >> 16
            return Akc.Bitwise.WORDBITS(x) - Akc.Bitwise.BitMinValue(x)

        @staticmethod
        def HIWORD(n):
            return (n >> 16) & 0xffff

        @staticmethod
        def LOWORD(n):
            return n & 0xffff

#C# TO PYTHON CONVERTER TODO TASK: There is no preprocessor in Python:
        ##endregion metot

#class Akc: #this class replaces the original namespace 'Akc'
    class ByteExtensions:
        @staticmethod
        def IsBitSet(b, pos):
            if pos < 0 or pos > 7:
                raise ArgumentOutOfRangeException("pos", "Index must be in the range of 0-7.")

            return (b & (1 << pos)) != 0

        @staticmethod
        def SetBit(b, pos):
            if pos < 0 or pos > 7:
                raise ArgumentOutOfRangeException("pos", "Index must be in the range of 0-7.")

            return int((b | (1 << pos)))

        @staticmethod
        def UnsetBit(b, pos):
            if pos < 0 or pos > 7:
                raise ArgumentOutOfRangeException("pos", "Index must be in the range of 0-7.")

            return int((b & ~(1 << pos)))

        @staticmethod
        def ToggleBit(b, pos):
            if pos < 0 or pos > 7:
                raise ArgumentOutOfRangeException("pos", "Index must be in the range of 0-7.")

            return int((b ^ (1 << pos)))

        @staticmethod
        def ToBinaryString(b):
            return Convert.ToString(b, 2).PadLeft(8, '0')
