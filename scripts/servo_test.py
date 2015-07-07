# coding: utf-8
"""
FutabaのRS405,RS406CB制御用ライブラリ
制御例
"""

import time
import rsc_u485
import sys

argvs = sys.argv
argc  = len(argvs)

if __name__ == '__main__':
    # メインルーチン
    servo = rsc_u485.RSC_U485('/dev/ttyUSB0',115200)
    
    if (argc < 2):   # 引数が足りない場合は、その旨を表示
        print 'Usage: # python %s filename' % argvs[0]
        quit()         # プログラムの終了

    i=int(argvs[1]);
    Range=int(argvs[2])

    print"サーボ番号%d,角度を%d度動かそうとしている" %(i, Range)

    servo.torque(i, 1)
     
    print '最高速度で%d度の位置へ回転' %Range

    print'ID%dのサーボのトルクをオン' %i
    servo.move(i, 900,4)
 
    time.sleep(5) # しばし待つ

    print '現在角度:%d' %servo.getAngle(l)
         
    print '1秒かけて0度の位置へ'
    servo.move(l,0,100)
     
    time.sleep(10)
