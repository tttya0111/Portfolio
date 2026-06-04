const video = document.getElementById('videoPlayer');
  const audio = document.getElementById('audioPlayer');

  video.addEventListener('play', function() {
    audio.play();
  });

  video.addEventListener('pause', function() {
    audio.pause();
  });

  video.addEventListener('ended', function() {
    audio.pause();
    video.currentTime = 0;
    audio.currentTime = 0;
  });