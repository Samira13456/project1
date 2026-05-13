from flask import Flask, render_template_string, request
from math import gcd

app = Flask(__name__)

# =========================
# АЛФАВИТЫ
# =========================

ENG_ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
RUS_ALPHABET = "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ"

ENG_LEN = len(ENG_ALPHABET)  # 26
RUS_LEN = len(RUS_ALPHABET)  # 33

# =========================
# ОБРАТНЫЙ ЭЛЕМЕНТ
# =========================

def mod_inverse(a, m):

    for x in range(1, m):

        if (a * x) % m == 1:
            return x

    return None

# =========================
# ПРОВЕРКА КЛЮЧА
# =========================

def check_key(a, alphabet_length):

    return gcd(a, alphabet_length) == 1

# =========================
# ШИФРОВАНИЕ
# =========================

def affine_encrypt(text, a, b):

    result = ""

    for char in text:

        upper_char = char.upper()

        # АНГЛИЙСКИЙ
        if upper_char in ENG_ALPHABET:

            x = ENG_ALPHABET.index(upper_char)

            encrypted = (a * x + b) % ENG_LEN

            new_char = ENG_ALPHABET[encrypted]

            if char.islower():
                new_char = new_char.lower()

            result += new_char

        # РУССКИЙ
        elif upper_char in RUS_ALPHABET:

            x = RUS_ALPHABET.index(upper_char)

            encrypted = (a * x + b) % RUS_LEN

            new_char = RUS_ALPHABET[encrypted]

            if char.islower():
                new_char = new_char.lower()

            result += new_char

        else:
            result += char

    return result

# =========================
# РАСШИФРОВКА
# =========================

def affine_decrypt(text, a, b):

    result = ""

    eng_inverse = mod_inverse(a, ENG_LEN)
    rus_inverse = mod_inverse(a, RUS_LEN)

    for char in text:

        upper_char = char.upper()

        # АНГЛИЙСКИЙ
        if upper_char in ENG_ALPHABET:

            if eng_inverse is None:
                return "Ошибка: ключ 'a' некорректен для английского алфавита"

            y = ENG_ALPHABET.index(upper_char)

            decrypted = (eng_inverse * (y - b)) % ENG_LEN

            new_char = ENG_ALPHABET[decrypted]

            if char.islower():
                new_char = new_char.lower()

            result += new_char

        # РУССКИЙ
        elif upper_char in RUS_ALPHABET:

            if rus_inverse is None:
                return "Ошибка: ключ 'a' некорректен для русского алфавита"

            y = RUS_ALPHABET.index(upper_char)

            decrypted = (rus_inverse * (y - b)) % RUS_LEN

            new_char = RUS_ALPHABET[decrypted]

            if char.islower():
                new_char = new_char.lower()

            result += new_char

        else:
            result += char

    return result

HTML = """
<!DOCTYPE html>
<html lang="ru">

<head>
<meta charset="UTF-8">
<title>Affine Cipher</title>

<style>

*{
    margin:0;
    padding:0;
    box-sizing:border-box;
}

body{
    font-family:Arial;
    background:linear-gradient(135deg,#0f172a,#1e293b,#334155);
    color:white;
    min-height:100vh;
    padding:40px;
}

.container{
    max-width:900px;
    margin:auto;
}

.card{
    background:rgba(255,255,255,0.08);
    backdrop-filter:blur(12px);
    border-radius:20px;
    padding:30px;
    margin-bottom:30px;
    box-shadow:0 0 25px rgba(0,0,0,0.4);
}

h1{
    text-align:center;
    margin-bottom:20px;
    color:#60a5fa;
    font-size:42px;
}

h2{
    margin-bottom:15px;
    color:#93c5fd;
}

p{
    line-height:1.7;
    margin-bottom:15px;
    color:#e2e8f0;
}

textarea{
    width:100%;
    min-height:130px;
    padding:15px;
    border:none;
    border-radius:12px;
    margin-bottom:15px;
    font-size:16px;
}

input{
    width:100%;
    padding:12px;
    border:none;
    border-radius:12px;
    margin-bottom:15px;
    font-size:16px;
}

.buttons{
    display:flex;
    gap:15px;
}

button{
    flex:1;
    padding:14px;
    border:none;
    border-radius:12px;
    font-size:16px;
    cursor:pointer;
    transition:0.3s;
    font-weight:bold;
}

.encrypt{
    background:#22c55e;
    color:white;
}

.encrypt:hover{ckground:#16a34a;
}

.decrypt{
    background:#3b82f6;
    color:white;
}

.decrypt:hover{
    background:#2563eb;
}

.result{
    margin-top:25px;
    background:#0f172a;
    padding:20px;
    border-radius:15px;
    border:1px solid #334155;
}

.info{
    background:#1e293b;
    padding:15px;
    border-radius:12px;
    margin-top:20px;
}

</style>
</head>

<body>

<div class="container">

<div class="card">

<h1>Афинный шифр</h1>

<p>
Сайт поддерживает:
</p>

<ul>
<li>Английский алфавит</li>
<li>Русский алфавит</li>
<li>Шифрование текста</li>
<li>Расшифровку текста</li>
<li>Проверку корректности ключей</li>
</ul>

<div class="info">

<p>
Для английского алфавита ключ a должен быть взаимно прост с 26.
</p>

<p>
Для русского алфавита ключ a должен быть взаимно прост с 33.
</p>

</div>

</div>

<div class="card">

<h2>Шифрование и расшифровка</h2>

<form method="POST">

<textarea
name="text"
placeholder="Введите текст..."
required
></textarea>

<input
type="number"
name="a"
placeholder="Введите ключ a"
required
>

<input
type="number"
name="b"
placeholder="Введите ключ b"
required
>

<div class="buttons">

<button
class="encrypt"
name="action"
value="encrypt"
>
Зашифровать
</button>

<button
class="decrypt"
name="action"
value="decrypt"
>
Расшифровать
</button>

</div>

</form>

{% if result %}

<div class="result">

<h2>Результат</h2>

<p>{{ result }}</p>

</div>

{% endif %}

</div>

</div>

</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def home():

    result = ""

    if request.method == "POST":

        text = request.form["text"]

        a = int(request.form["a"])
        b = int(request.form["b"])

        action = request.form["action"]

        # Проверка ключей

        has_eng = any(ch.upper() in ENG_ALPHABET for ch in text)
        has_rus = any(ch.upper() in RUS_ALPHABET for ch in text)

        if has_eng and not check_key(a, ENG_LEN):
            result = "Ошибка: ключ 'a' некорректен для английского алфавита"

        elif has_rus and not check_key(a, RUS_LEN):
            result = "Ошибка: ключ 'a' некорректен для русского алфавита"

        else:

            if action == "encrypt":
                result = affine_encrypt(text, a, b)

            elif action == "decrypt":
                result = affine_decrypt(text, a, b)

    return render_template_string(HTML, result=result)

if __name__ == "__main__":
    app.run(debug=True) 