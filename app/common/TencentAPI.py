# -*- coding: utf-8 -*-
# 腾讯API字典


TencentAPI={
    #基本文本分析API
    "nlp_wordseg":    {
        'APINAME':'分词', #API中文简称
        'APIDESC': '对文本进行智能分词识别，支持基础词与混排词粒度', #API描述
        'APIURL': 'https://api.ai.qq.com/fcgi-bin/nlp/nlp_wordseg', #API请求URL
        'APIPARA': 'text' #API非公共参数
    },
    "nlp_wordpos":    {
        'APINAME':'词性标注',
        'APIDESC': '对文本进行分词，同时为每个分词标注正确的词性',
        'APIURL': 'https://api.ai.qq.com/fcgi-bin/nlp/nlp_wordpos',
        'APIPARA': 'text'
    },
    'nlp_wordner':    {
        'APINAME':'专有名词识别',
        'APIDESC': '对文本进行专有名词的分词识别，找出文本中的专有名词',
        'APIURL': 'https://api.ai.qq.com/fcgi-bin/nlp/nlp_wordner',
        'APIPARA': 'text'
    },
    'nlp_wordsyn':    {
        'APINAME':'同义词识别',
        'APIDESC': '识别文本中存在同义词的分词，并返回相应的同义词',
        'APIURL': 'https://api.ai.qq.com/fcgi-bin/nlp/nlp_wordsyn',
        'APIPARA': 'text'
    },
    
    #计算机视觉--OCR识别API
    "ocr_generalocr":    {
        'APINAME':'通用OCR识别',
        'APIDESC': '识别上传图像上面的字段信息',
        'APIURL': 'https://api.ai.qq.com/fcgi-bin/ocr/ocr_generalocr',
        'APIPARA': 'image'
    },
    "ocr_idcardocr":    {
        'APINAME':'身份证OCR识别',
        'APIDESC': '识别身份证图像上面的详细身份信息',
        'APIURL': 'https://api.ai.qq.com/fcgi-bin/ocr/ocr_idcardocr',
        'APIPARA': 'image,card_type'
    },
    "ocr_bcocr":    {
        'APINAME':'名片OCR识别',
        'APIDESC': '识别名片图像上面的字段信息',
        'APIURL': 'https://api.ai.qq.com/fcgi-bin/ocr/ocr_bcocr',
        'APIPARA': 'image'
    },
    "ocr_driverlicenseocr":{
        'APINAME':'行驶证驾驶证OCR识别',
        'APIDESC': '识别行驶证或驾驶证图像上面的字段信息',
        'APIURL': 'https://api.ai.qq.com/fcgi-bin/ocr/ocr_driverlicenseocr',
        'APIPARA': 'image,type'
    },
    "ocr_bizlicenseocr":{
        'APINAME':'营业执照OCR识别',
        'APIDESC': '识别营业执照上面的字段信息',
        'APIURL': 'https://api.ai.qq.com/fcgi-bin/ocr/ocr_bizlicenseocr',
        'APIPARA': 'image'
    },
    "ocr_creditcardocr":{
        'APINAME':'银行卡OCR识别',
        'APIDESC': '识别银行卡上面的字段信息',
        'APIURL': 'https://api.ai.qq.com/fcgi-bin/ocr/ocr_creditcardocr',
        'APIPARA': 'image'
    },
    # lbp add
    "face_detectface":{
        'APINAME':'人脸检测与分析',
        'APIDESC': '识别上传图像上面的人脸信息',
        'APIURL': 'https://api.ai.qq.com/fcgi-bin/face/face_detectface',
        'APIPARA': 'image'
    }
}
