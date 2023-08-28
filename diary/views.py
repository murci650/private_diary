import logging

from django.urls import reverse_lazy
#URLを指定する際はreverse_lazy関数でURLのハードコーティングを避ける。
#reverse_lazy('<urls.pyのapp_name>:<ルーティングにつけたname>')

from django.shortcuts import render
from django.views import generic
from .forms import InquiryForm

logger = logging.getLogger(__name__)
#loggerを取得
#logger.<ログレベル>(<出力内容>]

class IndexView(generic.TemplateView):
    template_name = "index.html"

class InquiryView(generic.FormView):
    template_name = "inquiry.html"
    form_class = InquiryForm
    success_url = reverse_lazy('diary:inquiry')
    #FormViewはクラス変数にURLを指定するだけで、処理に問題が無かった時に指定URLにリダイレクトする

def form_valid(self, form):
#フォームバリデーションに問題なければ実行されるメソッド
#フォームバリデーションを通ったユーザ入力値を↓の形でとりだせる
#form.cleaded_data['<フィールド名>']
    form.send_email()
    #form.pyにメール送信メソッドを呼び出す
    logger.info('Inquiry sent by {}'.format(form.cleaned_data['name']))
    #ビューからログを出力
    return super().form_valid(form)