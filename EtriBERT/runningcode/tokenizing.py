import argparse
import json
import urllib3
from tqdm import tqdm

def parser_add_argument	( parser ) :

    ## Required parameters
    parser.add_argument("--openapi_key", default="key", type=str, required=True, help="OpenAPI key information for morphology analysis")
    ## Other parameters
    parser.add_argument("--input_file", default="../../data/law.json", type=str, help="all file that include train file and test file")
    parser.add_argument('--output_file', type=str, default="../../data/tokenizing.json", help="Tokenizing file")

    return parser

def do_lang(openapi_key, text):
    openApiURL = "http://aiopen.etri.re.kr:8000/WiseNLU"

    requestJson = {"access_key": openapi_key, "argument": {"text": text, "analysis_code": "morp"}}

    http = urllib3.PoolManager()
    response = http.request("POST", openApiURL, headers={"Content-Type": "application/json; charset=UTF-8"},
                            body=json.dumps(requestJson))

    return response.data.decode()


def main() :
    parser = argparse.ArgumentParser()
    parser = parser_add_argument(parser)
    args = parser.parse_args()

    APIkey = args.openapi_key
    # predefined question list
    questionList = ["피해자가 누구인가요?", "범행이 언제 발생했나요?", "범행이 어디서 발생했나요?", "어떤 범행이 발생했나요?"]

    with open(args.input_file) as json_file:
        json_data = json.load(json_file)

    num = 0
    Tokenized = {}

    for ques in questionList :
        Tokenized[ques] = do_lang(APIkey, ques)

    for paragraphs_title in tqdm(json_data['data']) :
        num += 1
        Tokenized[paragraphs_title['paragraphs'][0]['context']] = [do_lang(APIkey, paragraphs_title['paragraphs'][0]['context'])]

    with open(args.output_file, "w") as writer:
            writer.write(json.dumps(Tokenized, indent=4, ensure_ascii=False) + "\n")




if __name__ == "__main__":
	main()