
import math

class TCKimlik:
    @staticmethod
    def Dogrula(tcKimlikNo):


        if len(tcKimlikNo) != 11:
            return False

        ATCNO = None
        TcNo = None
        BTCNO = None
        C1 = None
        C2 = None
        C3 = None
        C4 = None
        C5 = None
        C6 = None
        C7 = None
        C8 = None
        C9 = None
        Q1 = None
        Q2 = None

        TcNo = long.Parse(tcKimlikNo)

        ATCNO = math.trunc(TcNo / float(100))
        BTCNO = math.trunc(TcNo / float(100))

        C1 = math.fmod(ATCNO, 10)
        ATCNO = math.trunc(ATCNO / float(10))
        C2 = math.fmod(ATCNO, 10)
        ATCNO = math.trunc(ATCNO / float(10))
        C3 = math.fmod(ATCNO, 10)
        ATCNO = math.trunc(ATCNO / float(10))
        C4 = math.fmod(ATCNO, 10)
        ATCNO = math.trunc(ATCNO / float(10))
        C5 = math.fmod(ATCNO, 10)
        ATCNO = math.trunc(ATCNO / float(10))
        C6 = math.fmod(ATCNO, 10)
        ATCNO = math.trunc(ATCNO / float(10))
        C7 = math.fmod(ATCNO, 10)
        ATCNO = math.trunc(ATCNO / float(10))
        C8 = math.fmod(ATCNO, 10)
        ATCNO = math.trunc(ATCNO / float(10))
        C9 = math.fmod(ATCNO, 10)
        ATCNO = math.trunc(ATCNO / float(10))
        Q1 = math.fmod((10 - math.fmod(((C1 + C3 + C5 + C7 + C9) * 3 + C2 + C4 + C6 + C8), 10)), 10)
        Q2 = math.fmod((10 - math.fmod(((C2 + C4 + C6 + C8 + Q1) * 3 + C1 + C3 + C5 + C7 + C9), 10)), 10)

        return BTCNO * 100 + Q1 * 10 + Q2 == TcNo


    @staticmethod
    def TCKontrolKodu(tcKimlikNo):
        returnvalue = ""
        ATCNO = 0
        C1 = None
        C2 = None
        C3 = None
        C4 = None
        C5 = None
        C6 = None
        C7 = None
        C8 = None
        C9 = None
        Q1 = None
        Q2 = None
        if len(tcKimlikNo) == 9:
            ATCNO = tcKimlikNo.AsUInt()

            C1 = math.fmod(ATCNO, 10)
            ATCNO = math.trunc(ATCNO / float(10))
            C2 = math.fmod(ATCNO, 10)
            ATCNO = math.trunc(ATCNO / float(10))
            C3 = math.fmod(ATCNO, 10)
            ATCNO = math.trunc(ATCNO / float(10))
            C4 = math.fmod(ATCNO, 10)
            ATCNO = math.trunc(ATCNO / float(10))
            C5 = math.fmod(ATCNO, 10)
            ATCNO = math.trunc(ATCNO / float(10))
            C6 = math.fmod(ATCNO, 10)
            ATCNO = math.trunc(ATCNO / float(10))
            C7 = math.fmod(ATCNO, 10)
            ATCNO = math.trunc(ATCNO / float(10))
            C8 = math.fmod(ATCNO, 10)
            ATCNO = math.trunc(ATCNO / float(10))
            C9 = math.fmod(ATCNO, 10)
            ATCNO = math.trunc(ATCNO / float(10))
            Q1 = math.fmod((10 - math.fmod(((C1 + C3 + C5 + C7 + C9) * 3 + C2 + C4 + C6 + C8), 10)), 10)
            Q2 = math.fmod((10 - math.fmod(((C2 + C4 + C6 + C8 + Q1) * 3 + C1 + C3 + C5 + C7 + C9), 10)), 10)

            returnvalue = str((Q1 * 10 + Q2)).PadLeft(2, '0')

        return returnvalue

    @staticmethod
    def OlabilirTc(tcKimlikNo):
        returnvalue = ""
        TcNo = None
        BTCNO = 0

        Durum = False

        if len(tcKimlikNo) == 11:
            TcNo = long.Parse(tcKimlikNo)
            BTCNO = math.trunc(TcNo / float(100))
            Durum = True

        if len(tcKimlikNo) == 9:
            BTCNO = tcKimlikNo.AsUInt()
            Durum = True

        if Durum:
            return str(BTCNO) + "-" + TCKimlik.TCKontrolKodu(str(BTCNO))

        return returnvalue



    @staticmethod
    def ileri(kimlik):
        num1 = None
        num2 = None
        num10 = None
        num11 = None
        rakam = [False for _ in range(8)]
        deger = None
        num1 = long.Parse(kimlik[0:5])
        num1 = num1 + 3

        num2 = long.Parse(kimlik[5:9])
        num2 = abs(num2 - 1)

        rakam[3] = True if kimlik[2:3] == str(num1).Substring(2, 1) else False

        rakam[7] = True if kimlik[6:7] == str(num2).PadLeft(4, '0')[1:2] else False

        num11 = int.Parse(kimlik[9:11])

        if rakam[3] == False:
            num11 = num11 + 10 - 6 if num11 < 6 else math.fmod((num11 - 6), 10)
        elif rakam[7] == False:
            num11 = num11 + 10 - 2 if num11 < 2 else math.fmod((num11 - 2), 10)
        else:
            num11 = num11 + 10 - 4 if num11 < 4 else math.fmod((num11 - 4), 10)

        num10 = 0
        i = 0
        while i < str(num1).Length:
            num10 += int(str(num1).Substring(i, 1))
            i += 1

        i = 0
        while i < str(num2).Length:
            num10 += int(str(num2).Substring(i, 1))
            i += 1

        num10 = math.fmod(num10, 10)

        num10 = num11 + 10 - num10 if num11 < num10 else num11 - num10

        #             if (num1.ToString().Length != 5 )
        #             {
        #                 MessageBox.Show("num1 hata " + num1.ToString())
        #             }
        #             if ( num2.ToString().Length != 4)
        #             {
        #                 MessageBox.Show("num2 hata " + num2.ToString())
        #             }
        #             

        deger = ""
        # deger = (num1.ToString().Length != 5 ? new string('0', 5 - num1.ToString().Length) + num1.ToString() : num1.ToString())
        #deger += (num2.ToString().Length != 4 ? new string('0', 4 - num2.ToString().Length) + num2.ToString() : num2.ToString())
        deger = str(num1).PadLeft(5, '0')
        deger += str(num2).PadLeft(4, '0')

        deger += str(num10)
        deger += str(num11)
        return deger
        #  return num1.ToString() + num1.ToString() + num10.ToString() + num11.ToString()
        #return (num1.ToString() + "--" +  num1.ToString() + "--" + num10.ToString() + "--" + num11.ToString())

    @staticmethod
    def geri(kimlik):
        num1 = None
        num2 = None
        num10 = None
        num11 = None
        rakam = [False for _ in range(8)]
        deger = None
        num1 = long.Parse(kimlik[0:5])
        num1 = num1 - 3

        num2 = long.Parse(kimlik[5:9])
        num2 = num2 + 1

        rakam[3] = True if kimlik[2:3] == str(num1).Substring(2, 1) else False

        rakam[7] = True if kimlik[6:7] == str(num2).PadLeft(4, '0')[1:2] else False

        num11 = int.Parse(kimlik[9:11])

        if rakam[3] == False:
            num11 = math.fmod((num11 + 6), 10)
        elif rakam[7] == False:
            num11 = math.fmod((num11 + 2), 10)
        else:
            num11 = math.fmod((num11 + 4), 10)

        num10 = 0
        i = 0
        while i < str(num1).Length:
            num10 += int(str(num1).Substring(i, 1))
            i += 1

        i = 0
        while i < str(num2).Length:
            num10 += int(str(num2).Substring(i, 1))
            i += 1

        num10 = math.fmod(num10, 10)

        num10 = num11 + 10 - num10 if num11 < num10 else num11 - num10

        #             if (num1.ToString().Length != 5 )
        #             {
        #                 MessageBox.Show("num1 hata " + num1.ToString())
        #             }
        #             if ( num2.ToString().Length != 4)
        #             {
        #                 MessageBox.Show("num2 hata " + num2.ToString())
        #             }
        #             

        deger = ""
        deger = str('0', 5 - str(num1).Length) + num1 if str(num1).Length != 5 else str(num1)
        deger += str('0', 4 - str(num2).Length) + num2 if str(num2).Length != 4 else str(num2)
        deger += str(num10)
        deger += str(num11)
        return deger
        #  return num1.ToString() + num1.ToString() + num10.ToString() + num11.ToString()
        #return (num1.ToString() + "--" +  num1.ToString() + "--" + num10.ToString() + "--" + num11.ToString())


