# AI law

## 1. preprocess data

data-processing 폴더 안에 있는 preprocess.py 실행시 excel 파일을 json 형태인 train set, test set, all set으로 변환

* train set : 70% data
* test set : 30% data
* all set  : 100% data

```
python3 preprocess.py 
--input_file ../data/law.xlsx
--output_dir ../data/
```



## 2. multilingual-BERT

multilingualBERT/runningcode 폴더 안에 있는 run_squad.py 실행시 입력 인자로 받은 train_file을 이용하여 학습을 한 뒤
predict_file로 모델 평가를 한다. predict_file에 대한 f1 score와 exact match score를 결과로 보여준다.
output_dir인 결과 폴더 안에는 예측 결과가 들어 있는 predictions.json,
fine tuning 을 거친 모델인 pytorch_model.bin 등아 생성된다.

``` 
python3 run_squad.py 
--model_type bert 
--model_name_or_path bert-base-multilingual-uncased 
--do_train 
--do_lower 
--do_eval 
--train_file ../../data/train.json 
--predict_file ../../data/test.json 
--per_gpu_train_batch_size 12 
--learning_rate 3e-5 
--num_train_epochs 2.0 
--max_seq_length 384 
--doc_stride 128 
--overwrite_output 
--overwrite_cache 
--output_dir ../../outputDir/multilingual/ 
--save_steps 5000 
--make_cache_file False
```



## 3. ETRI-BERT

Etri의 KorBERT를 사용하기 위해서는 [이 사이트](http://aiopen.etri.re.kr/service_dataset.php)에서 사용허가협약서를 작성한 뒤 다운로드 받아야 합니다.
pretrained model은 개인이 따로 공개할 수 없어 업로드하지 않겠습니다.
모델을 다운받으신 후 EtriBERT 폴더에 넣어주세요.


### 3-1. 형태소 분석용 파일을 생성

EtriBERT를 사용하기 위해서는 Etri에서 제공하는 형태소 분석 API를 사용하여 형태소 분석된 결과를 사용하여 인풋으로 넣어줘야한다.
하지만 형태소 분석 API 호출은 하루 당 5000건으로 제한되어있다. 그래서 수집한 데이터 문장들을 미리 호출시켜 문장을 형태소 분석된 문장으로 바꿔주는 파일인 tokenizing.json을 생성.

* 모든 데이터가 들어있는 law.json 파일을 불러와서 API호출 후 tokenizing.json 파일을 만듬

```
python3 tokenizing.py
--openapi_key your key
--input_file ../../data/law.json 
--output_file ../../data/tokenizing.json

```

### 3-2. EtriBERT를 실행

EtriBERT 폴더 안에 있는 run_squad_ETRI.py 실행시 train set은 train.json, test set은 test.json, tokenizing file을 tokenizing.json으로 하여 f1 score와 exact match score를 프린트 해주고,
결과 폴더 안에 예측 결과가 들어 있는 predictions.json과 학습된 모델인 pytorch_model.bin을 생성

```
python3 run_squad_ETRI.py 
--openapi_key 6bc85742-7158-46c8-8d79-980033df4be7 
--bert_model .. 
--train_file ../../data/train.json 
--predict_file ../../data/test.json 
--output_dir ../../outputDir/EtriBERT 
--tokenized_file ../../data/tokenizing.json 
--do_train 
--do_predict
```

openapi_key는 etri API DATA 서비스 포털에서 발급 가능
이 키를 사용하면 형태소 분석 API 호출이 가능하고, Etri BERT 모델을 다운로드 가능

## 4. Result

한국어만을 사용해 학습한 뒤 형태소 분석기를 사용한 Etri의 KorBERT가 Multilingual BERT에 비해 전체적으로 높은 성능을 보였다.

![](./image/experiment_result.png)