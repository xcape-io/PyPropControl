for %%f in (*.wav) do (

  ffmpeg.exe -i %%~nf.wav -r 22050 -y %%~nf.22k.wav
)