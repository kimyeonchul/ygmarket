function getRandomPosition() {
  var pageHeight = document.documentElement.scrollHeight;
  var windowWidth = $(window).width()-100;
    var minHeight = 200; // 최소 높이
  var maxHeight = pageHeight - 100; // 최대 높이
  var top = Math.random() * (maxHeight - minHeight) + minHeight;
 var leftRanges = [
    { min: 0, max: windowWidth*0.2 },
    { min: windowWidth*0.8, max: windowWidth }
  ];
  var randomRange = leftRanges[Math.floor(Math.random() * leftRanges.length)];
  var left = Math.random() * (randomRange.max - randomRange.min) + randomRange.min;
  return {
    top: top,
    left: left
  };
}

function getRandomRotation() {
  var rotation = Math.random() * 360; // 0도부터 360도까지의 랜덤한 회전 값을 생성합니다.
  return rotation;
}

for (var i = 0; i < 3; i++) {
    var img = $(`#base_mascot_image${i+1}`);
  var randomPosition = getRandomPosition();
  var randomRotation = getRandomRotation();

  img.css({
    position: "absolute",
    top: randomPosition.top,
    left: randomPosition.left,
      "z-index":-1,
      transform: "rotate(" + randomRotation + "deg)" // 랜덤한 회전 값을 적용합니다.
  });
}