import os

from django import forms
from django.core.mail import EmailMessage
#django.coe.mail.Email.EmailMessageクラスを使ってメール送信する
#このクラスはBccやメール添付も行うことができる。取扱いが難しいこともない。

class InquiryForm(forms.Form):
    name = forms.CharField(label='お名前',max_length=30)
    email = forms.EmailField(label='メールアドレス')
    title = forms.CharField(label='タイトル',max_length=30)
    message = forms.CharField(label='メッセージ',widget=forms.Textarea)

    def send_email(self):
        name = self.cleaned_data['name']<!-- 2-->
#引数のselfから「self.cleaned_data'<フィールド名>'のようにして、前節のビューの時と同様にフォームバリデーションを通ったユーザ入力値を取得できる
        email = self.cleaned_data['email']
        title = self.cleaned_data['title']
        message = self.cleaned_data['message']

        subject = 'お問い合わせ{}'.format(title)
        message = '送信者名:{0}?\nメールアドレス:{1}\nメッセージ:\n{2}'.format(name, email, message)
        from_email = os.environ.get('FROM_EMAIL')
#送信元(from_email)と宛先(to_list)は、settings.pyで設定されたデータベースパスワードのように環境変数からセットする
        to_list = [
            os.environ.get('FROM_EMAIL')
#送信元from_emailと宛先to_listはsettings.pyで設定したデータベースのパスワードのように環境変数からセットする。
#ただし開発環境では、これらの値がブランクでも動作に支障がないためPyCharmで環境変数を設定している
        ]
        cc_list = [
            email
        ]
        message = EmailMessage(subject=subject, body=message, from_email=from_email, to=to_list, cc=cc_list)<!-- 4--><!-- -->
        message.send()<!-- 5--><!-- -->
#EmailMessageインスタンスを作成して、sendメソッドを呼び出す

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['name'].widget.attrs['class'] = 'form-control'
        self.fields['name'].widget.attrs['placeholder'] = 'お名前を入力して下さい'
        self.fields['email'].widget.attrs['class'] = 'form-control'
        self.fields['email'].widget.attrs['placeholder'] = 'メールアドレスを入力して下さい'
        self.fields['title'].widget.attrs['class'] = 'form-control'
        self.fields['title'].widget.attrs['placeholder'] = 'タイトルを入力して下さい'
        self.fields['message'].widget.attrs['class'] = 'form-control'
        self.fields['message'].widget.attrs['placeholder'] = 'メッセージを入力して下さい'

# __init__メソッドの中でself.fieldを編集することでcss属性を操作している
# 操作内容はBootstrapのフォーム用クラスform-controlとplaceholderを追加している





