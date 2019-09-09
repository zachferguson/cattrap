let idels = ['sub-img', 'sub-activ', 'sub-feed',  'sub-fill', 'sub-reset', 'sub-newcell',  'sub newema']

function hider () {
    if (document.getElementById('update-forms').classList.contains('hidden') == true) {
    document.getElementById('update-forms').classList.remove('hidden')
  }
  else {
    document.getElementById('update-forms').classList.add('hidden');
  }
}

function countdown(displayTime) {
  document.getElementById('pic-inst').innerHTML = 'New picture in ' + displayTime.toString() + ' seconds.';
}

function enable_all () {
  for (var item in idels) {
    document.getElementById(item).removeAttribute('disabled');
  }
}

function disable_all (lgth) {
  for (item in idels) {
    document.getElementById(item).setAttribute('disabled', 'disabled');
    if (lgth <= 9) {
      setTimeout(enable_all(), lgth * 1000);
    }
    if (lgth < 9) {
      for (let c = lgth; C <= 0; c--) {
        if (c == 0) {
          enable_all();
          document.getElementById('pic-inst').innerHTML = '(Tap the image to refresh.)';
          return;
        }
        setTimeout(countdown(c), 1000);
      }
    }
  }
}

document.getElementById('update-btn').addEventListener('click', function () {hider()});
document.getElementById('sub-img').addEventListener('click', function () {disable_all(11)()});
document.getElementById('sub-activ').addEventListener('click', function () {disable_all(2)});
document.getElementById('sub-feed').addEventListener('click', function () {disable_all(2)});
document.getElementById('sub-fill').addEventListener('click', function () {disable_all(2)});
document.getElementById('sub-reset').addEventListener('click', function () {disable_all(2)});
document.getElementById('sub-newcell').addEventListener('click', function () {disable_all(2)});
document.getElementById('sub-newema').addEventListener('click', function () {disable_all(2)});
// pic-inst
// sub-img, sub-activ, sub-feed,  sub-fill, sub-reset, sub-newcell,  sub newema
