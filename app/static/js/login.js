let selectEl = document.getElementById('rank');

selectEl.addEventListener('change', (e) => {
  if (e.target.value == 'Student') {
    document.getElementById('year-input').style.display = 'block';
  } else {
    document.getElementById('year-input').style.display = 'none';
  }
});

let selectElDos = document.getElementById('rank');

selectEl.addEventListener('change', (e) => {
  if (e.target.value == 'Teacher') {
    document.getElementById('teacher-notif').style.display = 'inline';
  } else {
    document.getElementById('teacher-notif').style.display = 'none';
  }
});