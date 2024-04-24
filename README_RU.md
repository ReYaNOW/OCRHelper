[![Linter check](https://github.com/ReYaNOW/OCRHelper/actions/workflows/pyci.yml/badge.svg)](https://github.com/ReYaNOW/OCRHelper/actions/workflows/action_tests.yml)
[![Maintainability](https://api.codeclimate.com/v1/badges/f5372d1edda7c846d573/maintainability)](https://codeclimate.com/github/ReYaNOW/OCRHelper/maintainability)
![Static Badge](https://img.shields.io/badge/total_lines-2.2k-blue)


<p align="center">
  <img src="https://raw.githubusercontent.com/ReYaNOW/ReYaNOW/main/OCR_Helper.png" alt="image"/>
</p>

<p align="center"><a href="https://github.com/ReYaNOW/OCRHelper/blob/main/README.md"><b>EN</b></a> | <b>RU</b></p>
<p align="center">Продвинутый экранный помощник. <b>OCRHelper</b> способен переводить текст из выделенной области. Еще есть возможность поиска значения слова при помощи ChatGPT, а также простого копирования в буфер обмена.</p>

<h1>Главные особенности</h1>
<ul>
<li><b>Высокая точность распознавания текста</b></li>
  OCR Helper для распознавания текста использует EasyOCR, который справляется с большинством ежедневных требований к считыванию текста.
  <li><b>Простой интерфейс</b></li>
  Основным принципом разработки было сделать предельно универсальное приложение без необходимости подгонки настроек под каждый отдельный случай изображения.
  <li><b>Доступные переводчики:</b> Google Translate, ChatGPT, ChatGPT с потоковым отображением</li>
  <li><b>Доступные языки для распознавания:</b> Русский, Английский, Японский</li>
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
  <li>1 GB свободной ОЗУ</li>
  <li>5 GB свободного места на диске / 1 GB для режима без CUDA</li>
  <li>Nvidia GPU с поддержкой CUDA SDK 11.8 (GTX 750, 8xxM, 9xx серия или новее) <i>(для режима с использованием CUDA)</i></li>
</ul>

<h1>Как использовать</h1>
<img src="https://github.com/ReYaNOW/repo_for_gifs/blob/main/ocrhelper/demo.gif?raw=true" alt="">
<ol>
<li>Выберите версию, подходящую для вас: обычная версия весит больше и запускается дольше, но быстрее считывает текст, у версии no_cuda все наоборот (скачать любую из них <a href="https://github.com/ReYaNOW/OCRHelper/releases">можно тут</a>)</li>
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
<h3>Следует установить не стандартный шрифт</h3>
<p>Это следует сделать для лучшего отображения окна приложения</p>
<p>Для это зайдите в "ocrhelper/additional files", запустите "Rubik.ttf", нажмите "установить"</p>
<h3>Используйте Безрамочный/Оконный режимы в играх (не Полноэкранный)</h3>
<p>Это необходимо, чтобы окно оверлея с переводом корректно отображалось поверх окна игры.</p>
<p>Если в игре не предусмотрена такая настройка, можете использовать сторонние программы (например, <a href="https://github.com/Codeusa/Borderless-Gaming">Borderless Gaming</a>)</p>
<h3>Устанавливайте приложение на SSD</h3>
<p>Это существенно снизит время запуска приложения.</p>
<h3>Ошибка</h3>
<p>Если возникла ошибка при работе приложения, пожалуйста создайте новый issue во вкладке Issues. Я постараюсь отреагировать на проблему, как только ее увижу.</p>

<h1>TODO</h1>
<ul>
  <li>Перевести приложение с Tkinter на PyQT</li>
  <li>Добавить поддержку геймпада для выделения области</li>
</ul>

<h1>Для разработки</h1>
<ul>
  <li>Склонировать репозиторий</li>
  
```bash
git clone https://github.com/ReYaNOW/OCRHelper.git
```
  <li>Установить зависимости</li>

```bash
make install
```  
Или
```bash
make install_without_cuda
```
</ul>

<h1>Зависимости</h1>
<ul>
  <li><a href="https://www.python.org/">Python 3.11+</a></li>
  <li><a href="https://python-poetry.org/">Poetry</a></li>
  <li>Библиотеки Python</li>
    <ul>
      <li><a href="https://github.com/TomSchimansky/CustomTkinter">CustomTkinter</a></li>
      <li><a href="https://github.com/nidhaloff/deep-translator">Deep-translator</a></li>
      <li><a href="https://github.com/moses-palmer/pystray">Pystray</a></li>
      <li><a href="https://github.com/boppreh/keyboard">Keyboard</a></li>
      <li><a href="https://github.com/python-pillow/Pillow">Pillow</a></li>
      <li><a href="https://github.com/numpy/numpy">Numpy</a></li>
      <li><a href="https://github.com/asweigart/pyperclip">Keyring</a></li>
      <li><a href="https://github.com/Akascape/CTkMessagebox">CTkMessagebox</a></li>
    </ul>
</ul>
