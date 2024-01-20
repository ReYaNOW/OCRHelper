[![Linter check](https://github.com/ReYaNOW/OCRHelper/actions/workflows/pyci.yml/badge.svg)](https://github.com/ReYaNOW/OCRHelper/actions/workflows/action_tests.yml)
[![Maintainability](https://api.codeclimate.com/v1/badges/f5372d1edda7c846d573/maintainability)](https://codeclimate.com/github/ReYaNOW/OCRHelper/maintainability)
![Static Badge](https://img.shields.io/badge/total_lines-2.2k-blue)


<p align="center">
  <img src="https://media.discordapp.net/attachments/324178393161793536/1173191004577333318/OCR_Helper.png?ex=65630e44&is=65509944&hm=9eb2229a6a84c656b1a16ce61b9ae3b3d54a26994709345d91e5304349c98d76&=" alt="image"/>
</p>

<p align="center"><b>EN</b> | <a href="https://github.com/ReYaNOW/OCRHelper/blob/main/README_RU.md"><b>RU</b></a></p>
<p align="center">Advanced Screen Assistant. <b>OCRHelper</b> is able to translate text from the selected area. It is also possible to search for the meaning of a word using ChatGPT, as well as simply copy it to the clipboard.</p>

<h1>Main features</h1>
<ul>
<li><b>High text recognition precision</b></li>
  OCR Helper for text recognition uses EasyOCR, which handles most of the daily text reading requirements.
  <li><b>Simple interface</b></li>
  The main idea was to make tool, that does not require manual adjustments for each case and convenient for everyday use. 
  <li><b>Available translators:</b> Google Translate, ChatGPT, ChatGPT with streaming display</li>
  <li><b>Available recognition and translation languages:</b> English, Russian, Japanese</li>
  <li><b>Dictionary: </b>mode for finding the meaning of a word using ChatGPT</li>
  <li><b>Recognition: </b>mode for only text recognition, can be used with the option to copy text to the clipboard</li>
</ul>
<h1>System requirements</h1>
<ul>
  <li>Windows 10 build 19041 (20H1) / Windows 11</li>
  <li>DirectX11</li>
  <li>1 GB free RAM</li>
  <li>5 GB free storage space/ 3 GB for without_cuda version</li>
  <li>Nvidia GPU with CUDA SDK 11.8 support (GTX 750, 8xxM, 9xx series or later) <i>(for mode using CUDA)</i></li>
</ul>

<h1>How to use</h1>
<img src="https://github.com/ReYaNOW/repo_for_gifs/blob/main/ocrhelper/demo.gif?raw=true" alt="">
<ol>
<li>Choose the version that suits you: the regular version weighs more and takes more time to start, but reads text faster, the without_cuda version is the opposite (you can download any of them <a href="https://github.com/ReYaNOW/OCRHelper/releases">here</a>)</li>
<li>Launch the application (The first launch will take much longer than the subsequent ones)</li>
  <li>Open the menu using CTRL + ALT + X or via the tray</li>
  <li>Open the settings</li>
  <li>Select the necessary languages for recognition (the fewer selected, the more accurate the recognition)</li>
  <li>Select a translator (you will need to enter an API-key to use GPT)</li>
<li>(Optional) Change the color of the area selection in the palette</li>
  <li>Press CTRL + SHIFT + X to select an area and then translate</li>
  <li>Wait for the translation result</li>
</ol> 

<h1>Usage Tips</h1>
<h3>Should install a non-standard font</h3>
<p>This should be done to better display the application window</p>
<p>To do this, go to "ocrhelper/additional files", run "Rubik.ttf", click "install"</p>
<h3>Use Borderless/Windowed modes in games (not Fullscreen)</h3>
<p>It is necessary to display the translation window overlay correctly.</p>
<p>If the game doesn't have such mode, you can use external tools to make it borderless (e.g. <a href="https://github.com/Codeusa/Borderless-Gaming">Borderless Gaming</a>)</p>
<h3>Install the application on SSD</h3>
<p>To reduce cold launch time with enabled EasyOCR engine (loading large EasyOCR model into RAM).</p>

<h1>TODO</h1>
<ul>
  <li>Move app on PyQT</li>
  <li>Add gamepad support for selecting area</li>
</ul>

<h1>For dev</h1>
<ul>
  <li>Clone repository</li>
  
```bash
git clone https://github.com/ReYaNOW/OCRHelper.git
```
  <li>Install dependencies</li>

```bash
make install
```  
or
```bash
make install_without_cuda
```
</ul>

<h1>Dependencies</h1>
<ul>
  <li><a href="https://www.python.org/">Python 3.11+</a></li>
  <li><a href="https://python-poetry.org/">Poetry</a></li>
  <li>Python libraries</li>
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
  
