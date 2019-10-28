'''
dq_timetable.py
작성자: 도석현

조별 과제를 하기 위해서 팀원들끼리 겹치는 공강 시간을 찾는 프로그램입니다.
Divide and Conquer 전략을 사용했습니다.

INPUT 형식에 맞춘 txt 파일이 필요합니다.
----------------------------------------------------------------------
입력 예)
MON 0900-1145 1330-1445 1630-1745
TUE 1200-1315 1330-1445
WED 0900-1145 1500-1650
FRI 1500-1745
.
WED 1030-1145 1500-1700
THU 0900-1145 1330-1445
FRI 1300-1450 1600-1750 1800-2045
.
TUE 0900-1145 1500-1745
WED 1200-1445 1800-2045
THU 1030-1145 1500-1745
.
---------------------------------------------------------------------
- MON, TUE, WED, THU, FRI / 월~금까지의 요일만 다룹니다.
- 시간 INPUT의 최소 단위는 5분입니다.
- 시간의 상한선-하한선은 0900-2100입니다.
- '.' 기호를 사용하여 팀원을 구분합니다.


---------------------------------------------------------------------
'입력 예)'에 대한 출력 예)
MON 1145-1330 1445-1630 1745-2100
TUE 1745-2100
WED 1700-1800
THU 1145-1330 1745-2100
FRI 0900-1300
---------------------------------------------------------------------
- OUTPUT은 5분 단위가 아니라 하나의 긴 시간으로 출력됩니다.
- 공통되는 시간이 30분 미만일 경우에는 OUTPUT으로 출력되지 않습니다.


1) 팀원 수를 입력합니다.
2) INPUT 내용이 들어있는 txt 파일명을 입력합니다.
3) 팀원들끼리 겹치는 공강시간이 출력이 됩니다.
'''

memeberNumber = int(input("팀원 수 입력: "))
timeIndex = 12*12   # TODO 일반화 필요 (시간 당 5분 조각 개수)*(끝시간-시작시간)

# 현재 인덱스에 해당하는 시간이 빈 시간인지 나타내는 리스트 (공강:True, 수업: False)
MON = [[True for _ in range(timeIndex)] for _ in range(memeberNumber+1)]
TUE = [[True for _ in range(timeIndex)] for _ in range(memeberNumber+1)]
WED = [[True for _ in range(timeIndex)] for _ in range(memeberNumber+1)]
THU = [[True for _ in range(timeIndex)] for _ in range(memeberNumber+1)]
FRI = [[True for _ in range(timeIndex)] for _ in range(memeberNumber+1)]


# input이 저장되어 있는 텍스트 파일을 읽어와서 List로 바꿔줌
def readInputTxt():
    inputFileName = input('INPUT 파일명 입력: ')
    with open('./' + inputFileName + '.txt', 'r', encoding='utf-8-sig') as inputTxt:
        inputList = inputTxt.read().split('\n')     # 줄바꿈을 기준으로 나누어서 저장
    # inputList : ['MON 0900-1145 1330-1445 1630-1745', 'TUE 1200-1315 1330-1445', 'WED 0900-1145 1500-1650', 'FRI 1500-1745', '.', 'WED 1030-1145 1500-1700', 'THU 0900-1145 1330-1445', 'FRI 1300-1450 1600-1750 1800-2045', '.', 'TUE 0900-1145 1500-1745', 'WED 1200-1445 1800-2045', 'THU 1030-1145 1500-1745', '.']
    return inputList


# boolean list로 변환하기 전 전처리 작업
def preprocessInputList(inputList):
    currentMember = 0

    for i in inputList:
        if i == '.' :
            # .을 만나면 다음 멤버로 넘어감
            currentMember += 1
            continue
        else :
            splitList = []
            splitList = splitList + i.split(' ')    # 요일, 시간으로 이루어진 리스트를 만듦 (1차 Divide)
                                                    # splitList : ['MON', '0900-1145', '1330-1445', '1630-1745']
            convertToBoolList(splitList, currentMember)


# 각 멤버의 시간 자료를 Boolean 형태로 저장
def convertToBoolList(splitList, currentMember):
    day = splitList[0]  # 요일 보관
    del splitList[0]    # 요일 지움 ['0900-1145', '1330-1445', '1630-1745']

    for i in range(len(splitList)) :
        splitList[i] = splitList[i].split('-') # [['0900', '1145'], ['1330', '1445'], ['1630', '1745']]

    for i in range(len(splitList)) :
        # 수업 시작시간과 끝시간을 5분 단위의 index 번호로 쪼갬 (2차 Divide)
        startHour = int(int(splitList[i][0]) / 100)
        startMin = int(int(splitList[i][0]) % 100)
        endHour = int(int(splitList[i][1]) / 100)
        endMin = int(int(splitList[i][1]) % 100)
        startIndex = int((startHour - 9) * 12 + (startMin / 5))     # TODO: 9(시작시간)를 일반화시키기
        endIndex = int((endHour - 9) * 12 + (endMin / 5))

        # index 번호로 쪼갠 수업시간(빈 시간이 아니므로 False)을 처음 선언했던 리스트에 반영
        for indexToFalse in range(startIndex, endIndex) :
            if day == 'MON' :
                MON[currentMember][indexToFalse] = False
            elif day == 'TUE' :
                TUE[currentMember][indexToFalse] = False
            elif day == 'WED' :
                WED[currentMember][indexToFalse] = False
            elif day == 'THU' :
                THU[currentMember][indexToFalse] = False
            elif day == 'FRI' :
                FRI[currentMember][indexToFalse] = False


# and 연산을 통해 모든 멤버의 공통 시간 자료를 DAY[memeberNumber]에 저장 (Conquer)
def makeCommonTimeList():
    for memberIdx in range(memeberNumber) :
        for j in range(timeIndex) :
            MON[memeberNumber][j] = MON[memeberNumber][j] and MON[memberIdx][j]
            TUE[memeberNumber][j] = TUE[memeberNumber][j] and TUE[memberIdx][j]
            WED[memeberNumber][j] = WED[memeberNumber][j] and WED[memberIdx][j]
            THU[memeberNumber][j] = THU[memeberNumber][j] and THU[memberIdx][j]
            FRI[memeberNumber][j] = FRI[memeberNumber][j] and FRI[memberIdx][j]

# DAY[memeberNumber] 의 boolean형 자료 -> 시간 정보로 바꾸어 출력
def printCommonTime(DAY):
    startTime = 2400
    endTime = 0

    for index in range(timeIndex) :
        if DAY[index] == False :
            # startTime이 초기화 상태라면 다음 index로 continue
            if startTime == 2400:
                continue

            # 가능한 시간이 30분 이하라면, startTime을 초기화 하고 다음 index로 continue
            if (endTime - startTime) < 30 :
                startTime = 2400
                continue

            # endTime이 ##60꼴일 때, 변형하여 위의 if문과 똑같은 과정으로 한 번 더 검사
            if endTime % 100 == 0 :
                tempEndTime = endTime - 100 + 60
                if(tempEndTime - startTime) < 30 :
                    startTime = 2400
                    continue

            print('%04d-%04d' %(startTime, endTime), end = ' ')
            startTime = 2400    # 출력 후 초기화

        elif DAY[index] == True :
            # convertToBoolList에서 변환시켰던 index를, 다시 입력받았던 시간의 형태로 변환하는 과정
            hour = (9 + int(index/12)) * 100   # TODO: 9(시작시간) 일반화 필요
            min = (index % 12) * 5

            # startTime은 가장 작은 값으로 유지
            if startTime > (hour + min) :
                startTime = hour + min

            # endTime은 계속 변화함
            endTime = hour + min + 5
            # ex) 0960 -> 1000으로 만들어 줌
            if endTime % 100 == 60 :
                endTime = endTime + 100 - 60

            # 2045-2100(마지막 시간 조각)에 해당하는 인덱스를 처리
            if index == (timeIndex - 1) :
                # if DAY[index] == False 조건문에서 출력하기 전 시행했던 검사와 동일
                if (startTime != 2400) and (2060 - startTime) > 30 :        # TODO: 2060 (2100으로 넣으면 오류!!!) (끝시간) 일반화 필요
                    print('%04d-%04d' %(startTime, endTime))
                    break
                else :
                    print('')


inputList = readInputTxt()
preprocessInputList(inputList)
makeCommonTimeList()

print('MON', end = ' ')
printCommonTime(MON[memeberNumber])
print('TUE', end = ' ')
printCommonTime(TUE[memeberNumber])
print('WED', end = ' ')
printCommonTime(WED[memeberNumber])
print('THU', end = ' ')
printCommonTime(THU[memeberNumber])
print('FRI', end = ' ')
printCommonTime(FRI[memeberNumber])
