# convert excel to json

import xlrd
import json
import copy
import random
import argparse
import os

def load_data(fn) :
    wb=xlrd.open_workbook(fn)
    ws=wb.sheet_by_index(0)

    nrow = ws.nrows
    ncol = ws.ncols
    print("> Read excel file")
    print("row num :",nrow)
    print("col num :",ncol)

    return ws

def convertExcelToJson (excel, to_all) :
    questionList = [excel.cell_value(0, i) for i in range(excel.ncols)]
    qNum = {}

    for i in range(len(questionList)):
        if "?" in questionList[i]:
            qNum[i] = 0

    article = []
    answer = []

    dataList = []
    datatmp = {}

    paragraphList = []
    paragraphtmp = {}

    qasList = []
    qastmp = {}

    ansList = []
    anstmp = {}

    id = 0
    for row in range(2, excel.nrows):
        article.append(len(excel.cell_value(row, 2)))

        for col in range(3, excel.ncols, 2):
            if len(excel.cell_value(row, col)) > 0:
                qNum[col] += 1

                text = excel.cell_value(row, col)
                startNum = excel.cell_value(row, col + 1)

                anstmp['answer_start'] = startNum
                anstmp['text'] = text
                ansList.append(anstmp)
                anstmp = {}

                answer.append(len(text))

                qastmp['question'] = questionList[col]
                qastmp['answers'] = ansList
                qastmp['id'] = str(id)

                qasList.append(qastmp)

                ansList = []
                qastmp = {}
                id = id + 1

        paragraphtmp['context'] = excel.cell_value(row, 2).strip()
        paragraphtmp['qas'] = qasList

        paragraphList.append(paragraphtmp)
        qasList = []
        paragraphtmp = {}

        datatmp['title'] = excel.cell_value(row, 0).strip()
        datatmp['paragraphs'] = paragraphList
        dataList.append(copy.deepcopy(datatmp))

        paragraphList = []

    print("\n총 데이터(context) 개수 :", len(dataList))

    random.shuffle(dataList)

    lawdict = {}
    lawdict['data'] = dataList

    for idx, count in qNum.items() :
        print(questionList[idx] + " : " + str(count))

    with open(to_all, "w", encoding="utf-8") as make_file:
        json.dump(lawdict, make_file, ensure_ascii=False, indent="\t")

    return lawdict

def train_test_split(lawdict, to_trn, to_tst) :

    length = len(lawdict['data'])
    train_length = int(length * 0.7)

    train = {}
    trainList = []

    test = {}
    testList = []

    for i in range(train_length):
        trainList.append(lawdict['data'][i])

    for i in range(train_length, length):
        testList.append(lawdict['data'][i])

    print("\n> Train-Test-Split")
    print(" Train :", len(trainList), "Test :", len(testList))

    train['data'] = trainList
    test['data'] = testList

    with open(to_trn, "w", encoding="utf-8") as make_file:
        json.dump(train, make_file, ensure_ascii=False, indent="\t")

    with open(to_tst, "w", encoding="utf-8") as make_file:
        json.dump(test, make_file, ensure_ascii=False, indent="\t")


def parser_add_argument	( parser ) :
    parser.add_argument("--input_file", default="../data/law.xlsx", type=str, help="KorCL excel file")
    parser.add_argument("--output_dir", default="../data/", type=str, help="KorCL json file")

    return parser

def main() :

    parser = argparse.ArgumentParser()
    parser = parser_add_argument(parser)
    args = parser.parse_args()

    train_fn = os.path.join( args.output_dir, "train.json" )
    test_fn = os.path.join( args.output_dir, "test.json")
    all_fn = os.path.join( args.output_dir, "law.json" )

    law_excel = load_data(args.input_file)
    law_dict = convertExcelToJson(law_excel, all_fn)
    train_test_split(law_dict, train_fn, test_fn)

if __name__ == "__main__" :
    main()