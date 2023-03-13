from sqlalchemy.orm import Session

from src.models import *
from src.schemas import *

import openai
openai.api_key = "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"
def index(sentences:list[str]):
  messages=[
      {"role": "system","content": "次のそれぞれの文章に対して，問題文と答えをそれぞれ作成してください．ただし次のフォーマットのJSONで出力してください."},
      #{"role": "system","content": "次のそれぞれの文章に対して，穴埋め問題をそれぞれ作成してください．ただし次のフォーマットのJSONで出力してください."},
      {"role": "assistant", "content": "フォーマット"},
      {"role": "assistant", "content": "[{\"qustion\":問題, \"answer\": 答え}, {\"qustion\":問題, \"answer\": 答え}]"},
      #{"role": "assistant", "content": "[{\"qustion\":問題}, {\"qustion\":問題}]"},
  ]     
  for sentence in sentences:
      messages.append({
          "role": "assistant",
          "content": sentence
      })
  res = openai.ChatCompletion.create(
      model = "gpt-3.5-turbo",
      messages=messages
  )
  print(res)
  print(res["choices"][0]["message"]["content"])
  return res
  

