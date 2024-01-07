[![Maintainability](https://api.codeclimate.com/v1/badges/f5372d1edda7c846d573/maintainability)](https://codeclimate.com/github/ReYaNOW/OCRHelper/maintainability)
![Static Badge](https://img.shields.io/badge/total_lines-1.8k-blue)


<p align="center">
  <img src="https://media.discordapp.net/attachments/324178393161793536/1173191004577333318/OCR_Helper.png?ex=65630e44&is=65509944&hm=9eb2229a6a84c656b1a16ce61b9ae3b3d54a26994709345d91e5304349c98d76&=" alt="image"/>
</p>  

<h1>Главные особенности</h1>
<ul>
<li><b>Высокая точность распознавания текста</b></li>
  OCR Helper для распознавания текста использует EasyOCR, который справляется с большинством ежедневных требований к считыванию текста.
  <li><b>Простой интерфейс</b></li>
  Основным принципом разработки было сделать предельно универсальное приложение без необходимости подгонки настроек под каждый отдельный случай изображения.
  <li><b>Доступные переводчики:</b> Google Translate, ChatGPT, ChatGPT с потоковым отображением</li>
  <li><b>Доступные языки для распознавания:</b> русский, английский, японский</li>
  <li><b>Доступные языки для перевода:</b> русский (остальные будут добавлены в ближайшем будущем)</li>
  <li><b>Режим поиска выделенного слова в словаре</b></li>
  Еще не добавлен...
  <li><b>Режим перевода зашифрованной выделенной строки (Base64, ASCII, Азбука Морзе)</b></li>
  Еще не добавлен...
</ul>
<h1>Системные требования</h1>
<ul>
  <li>Windows 10 build 19041 (20H1) / Windows 11</li>
  <li>DirectX11</li>
  <li>8 GB ОЗУ</li>
  <li>5 GB свободного места на диске / 3 GB для режима без CUDA</li>
  <li>Nvidia GPU с поддержкой CUDA SDK 11.8 (GTX 750, 8xxM, 9xx серия или новее) <i>(для режима с использованием CUDA)</i></li>
</ul>

<h1>Как использовать</h1>
<img src="https://github.com/ReYaNOW/repo_for_gifs/blob/main/ocrhelper/demo.gif?raw=true" alt="">
<ol>
<li>Выберите версию, подходящую для вас: обычная версия весит больше и запускается дольше, но быстрее считывает текст, у версии no_cuda все наоборот (скачать любую из них можно тут https://github.com/ReYaNOW/OCRHelper/releases)</li>
<li>Запустите приложение (Первый запуск будет намного дольше последующих)</li>
  <li>Откройте меню при помощи CTRL + ALT + X или через трей</li>
  <li>Откройте настройки</li>
  <li>Выберите необходимые языки для распознавания (чем меньше выбрано, тем точнее распознавание)</li>
  <li>Выберите переводчик (для использования GPT необходимо будет ввести API-ключ)</li>
<li>(Опционально) Смените цвет выделения области в палитре</li>
  <li>Нажмите CTRL + SHIFT + X для выбора области и последующего перевода</li>
  <li>Дождитесь результата перевода</li>
</ol> 

<h1>Советы по использованию</h1>
<h3>Используйте Безрамочный/Оконный режимы в играх (не Полноэкранный)</h3>
<p>Это необходимо, чтобы окно оверлея с переводом корректно отображалось поверх окна игры.</p>
<p>Если в игре не предусмотрена такая настройка, можете использовать сторонние программы (например, <a href="https://github.com/Codeusa/Borderless-Gaming">Borderless Gaming</a>)</p>
<h3>Устанавливайте приложение на SSD</h3>
<p>Это существенно снизит время запуска приложения.</p>