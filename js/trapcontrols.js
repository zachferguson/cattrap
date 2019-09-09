let trapdata = {'8165010001': {'trapserial': '8165010001', 'cell': 5707046838, 'email': 'zach.ferguson@yahoo.com', 'activate': false, 'reset': false, 'foodcount': 6, 'image': '/trapper/8165010001.jpg'}, '8166010001': {'trapserial': '8166010002', 'cell': 5706068357, 'email': 'zach_f77@yahoo.com', 'activate': false, 'reset': false, 'foodcount': 6, 'image': '/trapper/8166010002.jpg'}};


function changetrapcellnumber() {
  console.log('change cell nunmber button pushed');
}
function changetrapemail() {
  console.log('change trap email button pushed');
}
function activatetrap() {
  console.log('activate trap button pushed');
}
function resettrap() {
  console.log('reset trap button pushed');
}
function activatefeeder() {
  console.log('activate feeder button pushed');
}

function populate(trapSerial) {
  // button names: changecell, changeemail, btnactivate, btnreset, btnfeeder
  // p names: displayp, trapcell, trapemail, foodremaining, instactivate, instreset, instfeeder

  if (document.getElementById('displaydiv').classList.contains('hidden')) {
    document.getElementById('displaydiv').classList.remove('hidden');
  }
  document.getElementById('trapcell').innerHTML = "Cell phone to text trap pictures to: " + trapdata[trapSerial]['cell'];
  document.getElementById('trapemail').innerHTML = "address to email trap pictures to: " + trapdata[trapSerial]['email'];
  document.getElementById('foodremaining').innerHTML = "Number of servings remaining in feeder: " + trapdata[trapSerial]['foodcount'];
  document.getElementById('changecell').addEventListener('click', function () {changetrapcellnumber()});
  document.getElementById('changeemail').addEventListener('click', function () {changetrapemail()});
  document.getElementById('btnactivate').addEventListener('click', function () {activatetrap()});
  document.getElementById('btnreset').addEventListener('click', function () {resettrap()});
  document.getElementById('btnfeeder').addEventListener('click', function () {activatefeeder()});

}
  function filler() {
    let trapSerial = document.getElementById('ser').value;
    if (trapSerial == "") {
    document.getElementById('displayp').innerHTML = "Please enter the trap's serial number.";
    return;
    }
    if (trapSerial in trapdata) {
     populate(trapSerial);
    }
  }
  document.getElementById('submitbtn').addEventListener('click', function () {filler()});
