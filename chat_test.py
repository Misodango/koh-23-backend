import openai
openai.api_key = "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"

def generate_cards(sentences:list[str]):
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

generate_cards(["教師なしの学習のもっとも単純な定義は，「データに内在するパターンを発見して活用することで飛行増加データに何らかの構造を与えるプロセス」である．", "データがランダムなプロセスによって生成されたものでなければ，多次元問題空間内のデータ要素の間に何らかのパターンが存在するはずだ．", "教師なし学習アルゴリズムは，これらのパターンを発見して活用することで，データセットに何らかの構造を与えるという仕組みになっている."])