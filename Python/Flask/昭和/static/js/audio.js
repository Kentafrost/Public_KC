$(function () {
    var audioBtn = $(".audio_button"),
      audioWrap = $(".audio_wrap"),
      audio = document.getElementById("audio");
  
    audioBtn.on("click", function () {
      if (audioWrap.hasClass("play")) {
        audio.pause();
        audioWrap.removeClass("play");
      } else {
        audio.play();
        audioWrap.addClass("play");
      }
    });
  });